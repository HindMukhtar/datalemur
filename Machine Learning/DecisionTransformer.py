import torch 
import torch.nn as nn 
import numpy as np 
from Attention import attention, multiheadAttention 
import math 

import torch
import torch.nn as nn
from torch.distributions import Categorical
import math

class PositionalEncoding(nn.Module):

    def __init__(self, d_model, max_len=5000):
        super().__init__()
        # Create positional encoding matrix
        pe = torch.zeros(max_len, d_model)
        # Position indices
        position = torch.arange(0, max_len).unsqueeze(1)
        # Compute frequency scaling
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
        )
        # Apply sin to even indices
        pe[:, 0::2] = torch.sin(position * div_term)
        # Apply cos to odd indices
        pe[:, 1::2] = torch.cos(position * div_term)
        # Add batch dimension
        pe = pe.unsqueeze(0)   # shape: [1, max_len, d_model]
        # Register as buffer (not trainable)
        self.register_buffer("pe", pe)

    def forward(self, x):
        """
        x shape: [batch_size, seq_len, d_model]
        """
        seq_len = x.size(1)
        # Add positional encoding
        x = x + self.pe[:, :seq_len]
        return x
    
class DecisionTransformer(nn.Module): 
    def __init__(self, 
                 state_dim, 
                 actions_dim, 
                 rtg_dim,
                 d_model, 
                 n_head,
                 n_layer,
                 max_len): 
        super().__init__() 
        self.state_dim = state_dim
        self.actions_dim = actions_dim
        self.rtg_dim = rtg_dim 

        self.d_model = d_model

        self.state_embed = nn.Linear(state_dim, d_model)
        self.actions_embed = nn.Linear(actions_dim, d_model)
        self.return_embed = nn.Linear(rtg_dim, d_model)
        self.time_embed = nn.Linear(max_len, d_model)

        self.pe = PositionalEncoding(max_len = max_len)

        self.output_embedding = nn.Linear(d_model, actions_dim)

        encoder_layer = nn.TransformerEncoderLayer(d_model, 
                                                   n_head, 
                                                   batch_first=True)
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layer)

    def forward(self, state, action, rtg, time): 
        batch_size, seq_len, _ = state.shape
        state = self.state_embed(state) # (batch_size, seq_len, d_model)
        action = self.actions_embed(action) # (batch_size, seq_len, d_model)
        rtg = self.return_embed(rtg) # (batch_size, seq_len, d_model)
        time = self.time_embed(time) # (batch_size, seq_len, d_model)

        state = state + time 
        action = action + time 
        rtg = rtg + time 

        x = torch.stack([rtg, state, action], dim = 2)
        x = x.reshape([batch_size, seq_len*3, self.d_model])

        causal_mask = torch.triu(
            torch.ones(seq_len*3, seq_len*3, device=x.device), diagonal=1
        ).bool()

        x = self.encoder(x, mask = causal_mask)
        x = x.reshape(batch_size, seq_len, 3, self.d_model)
        state_tokens = x[:, :, 1, :]

        action_preds = self.output_embedding(state_tokens)

        return action_preds
    

class OnlineDecisionTransformer(nn.Module): 
    def __init__(self, 
                 env,
                 state_dim, 
                 actions_dim, 
                 rtg_dim,
                 d_model, 
                 n_head,
                 n_layer,
                 batch_size, 
                 max_len, 
                 buffer_size, 
                 learning_rate, 
                 gamma): 
        super().__init__() 
        self.env = env
        self.state_dim = state_dim 
        self.actions_dim = actions_dim 
        self.rtg_dim = rtg_dim 
        self.d_model = d_model 
        self.n_head = n_head 
        self.n_layer = n_layer 
        self.batch_size = batch_size 
        self.max_len = max_len
        self.buffer_size = buffer_size 
        self.lr = learning_rate
        self.gamma = gamma
        self.buffer = []
        self.DT = DecisionTransformer(state_dim, 
                                      actions_dim, 
                                      rtg_dim, 
                                      d_model, 
                                      n_head, 
                                      n_layer, 
                                      max_len)
        
    def calculate_rtg(self, rewards): 
        rtg = np.zeros(len(rewards))
        rtn = 0 

        for i in reversed(rewards): 
            rtn += rewards 
            rtg[i] = rtn 

        return rtg 

    
    def collect_episode(self, target_return): 
        obs, info = self.env.reset() 

        states = []
        actions = []
        rewards = []
        rtgs = []
        timesteps = []

        step = 0 
        done = False 

        desired_return = float(target_return)

        while not done and step < self.max_len: 

            # build history up to current step 
            states_hist = states + torch.tensor(obs)
            time_hist = timesteps + torch.tensor(step)

            # build action history and shift to prevent including current action in history 
            actions_hist = [0] + actions 
            actions_hist = actions_hist[:len(states_hist)]

            # use target return to build RTG history 
            rtg_hist = rtgs + [desired_return]

            # convert tensors dims for input to ODT 
            states_tensor = states_hist.unsqueeze(0) # 1, seq_len, state_dim 
            actions_tensor = actions_hist.unsqueeze(0) # 1, seq_len
            rtg_tensor = rtg_hist.view(states_hist.shape[0], states_hist.shape[1], 1)
            time_tensor = time_hist.unsqueeze(0) # 1, seq_len 

            with torch.no_grad(): 
                actions_logits = self.DT(states_tensor, actions_tensor, rtg_tensor, time_tensor)
                # actions_logits shape is B, T, actions_dim 
                current_logits = actions_logits[0, -1] # we only want the prediction for the last step 
                action_dist = Categorical(logits=current_logits)
                action = action_dist.sample().item() 

            # step environment with action 
            next_obs, reward, terminated, truncated = self.env.step(action)
            done = terminated or truncated  

            states.append(torch.tensor(obs))
            timesteps.append(torch.tensor(step))
            actions.append(actions)
            rewards.append(reward)

            step+=1
            desired_return = target_return - reward 
            obs = next_obs 

        # calculate rtgs 
        rtgs = self.calculate_rtg(rewards)

        episode = {
            "states": torch.stack(states),                                # (T, state_dim)
            "actions": torch.tensor(actions, dtype=torch.long),           # (T,)
            "rtgs": torch.tensor(rtgs, dtype=torch.float32).unsqueeze(-1),# (T, 1)
            "timesteps": torch.tensor(timesteps, dtype=torch.long),       # (T,)
        }
        return episode

    def sample_batch(self):
        # very simple version: sample full episodes and pad/truncate
        batch_eps = self.buffer[:self.batch_size]

        states_batch = []
        actions_batch = []
        rtgs_batch = []
        times_batch = []

        for ep in batch_eps:
            T = min(len(ep["actions"]), self.max_len)

            states = ep["states"][:T]
            actions = ep["actions"][:T]
            rtgs = ep["rtgs"][:T]
            times = ep["timesteps"][:T]

            # pad if needed
            if T < self.max_len:
                pad_len = self.max_len - T
                states = torch.cat([states, torch.zeros(pad_len, self.state_dim)], dim=0)
                actions = torch.cat([actions, torch.zeros(pad_len, dtype=torch.long)], dim=0)
                rtgs = torch.cat([rtgs, torch.zeros(pad_len, 1)], dim=0)
                times = torch.cat([times, torch.zeros(pad_len, dtype=torch.long)], dim=0)

            states_batch.append(states)
            actions_batch.append(actions)
            rtgs_batch.append(rtgs)
            times_batch.append(times)

        states_batch = torch.stack(states_batch)      # (B, T, state_dim)
        actions_batch = torch.stack(actions_batch)    # (B, T)
        rtgs_batch = torch.stack(rtgs_batch)          # (B, T, 1)
        times_batch = torch.stack(times_batch)        # (B, T)

        return states_batch, actions_batch, rtgs_batch, times_batch

    def learn(self, max_updates, target_return): 

        optimizer = torch.optim.Adam(self.DT.parameters(), self.lr)
        loss_fn = nn.CrossEntropyLoss() 

        # fill initial buffer 
        while len(self.buffer) < self.buffer_size: 
            episode = self.collect_episode(self.max_len)
            self.buffer.append(episode)

        
        for i in range(max_updates): 
            # sample batch 
            states, target_actions, target_returns, timesteps = self.sample_batch() 

            prev_actions = torch.zeros_like(target_actions)
            prev_actions[:, 1:] = target_actions[:, :-1]

            pred_logits = self.DT(states, prev_actions, target_returns, timesteps)
            # pred_logits: (B, T, action_dim)

            B, T, A = pred_logits.shape
            loss = loss_fn(
                pred_logits.reshape(B * T, A),
                target_actions.reshape(B * T)
            )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            


        




            



            











