import torch 
import torch.nn as nn 
import numpy as np 
import gymnasium as gym
from gymnasium import spaces
from collections import deque
import random 

class Environment(gym.Env): 
    def __init__(self): 
        super().__init__()
        self.current_step = 0 
        self.eps_length  = 0 

    def step(self, action): 
        # take action 
        obs = self._getobs()
        reward = self._getreward() 
        terminated = False 
        truncated = False 
        if self.current_step > self.eps_length: 
            terminated = True 
        
        return obs, reward, terminated, truncated

    def reset(self): 
        return 

    def _getobs(self): 
        obs = []
        return obs 

    def _getreward(self): 
        reward = 1 
        return reward

class QNetwork(nn.Module): 
    def __init__(self, input_dim, output_dim, d_model, n_layers):
        super().__init__() 
        self.input_dim = input_dim 
        self.output_dim = output_dim 
        self.d_model = d_model 
        self.n_layers = n_layers 
        self.input_layer = nn.Linear(input_dim, d_model)
        self.hidden_layers = nn.ModuleList([])
        for _ in range(n_layers): 
            self.hidden_layers.append(nn.Linear(d_model, d_model))
        self.output_layers = nn.Linear(d_model, output_dim)

    def forward(self, x): 
        out = self.input_layer(x)
        for _ in range(self.n_layers): 
            out = self.hidden_layers(out)
        out = self.output_layers(out)
        return out 


class DQN(nn.Module): 
    def __init__(self, 
                 env, 
                 obs_dim, 
                 action_dim, 
                 d_model, 
                 n_layers,
                 batch_size, 
                 learning_rate,
                 discount_factor, 
                 buffer_size, 
                 target_updates, 
                 learning_start, 
                 epsilon, 
                 epsilon_min, 
                 epsilon_decay):
        super().__init__()
        self.env = env
        self.obs_dim = obs_dim 
        self.action_dim = action_dim
        self.batch_size = batch_size 
        self.lr = learning_rate 
        self.gamma = discount_factor 
        self.buffer_size = buffer_size 
        self.target_updates = target_updates 
        self.learning_start = learning_start 
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min 
        self.epsilon_decay = epsilon_decay
        self.qnet = QNetwork(obs_dim, action_dim, d_model, n_layers)
        self.targetnet = QNetwork(obs_dim, action_dim, d_model, n_layers)

    def learn(self, epochs): 
        epochs
        self.buffer = deque(maxlen=self.buffer_size) # (state, action, reward, st+1)
        step = 0 
        obs, info = self.env.reset()
        loss_fn = nn.MSELoss() 
        optimizer = torch.optim.Adam(self.qnet.parameters(), lr=self.lr)

        for _ in range(epochs): 
            obs = torch.tensor(obs)
            q = self.qnet.forward(obs)
            if random.random() < self.epsilon: 
                # select random action
                action = random.randrange(self.action_dim)
            else: 
                action = torch.argmax(q)
            next_obs, reward, terminated, truncated, info = self.env.step(action.item())
            done = terminated or truncated
            self.buffer.append((obs, action, reward, next_obs, done))
            obs = next_obs 

            if len(self.buffer) >= self.batch_size: 
                batch = random.sample(self.buffer, self.batch_size)
                obs_batch, action_batch, reward_batch, next_obs_batch, done_batch = zip(*batch)

                action_batch = torch.tensor(action_batch, dtype=torch.long)
                q = self.qnet.forward(obs_batch)
                q_taken = q.gather(dim=1, index=action_batch.unsqueeze(1)).squeeze(1)
                next_obs_batch = torch.tensor(next_obs_batch)
                future_val = self.targetnet.forward(next_obs_batch)
                future_val = future_val.max(dim=1)
                target = torch.tensor(reward) + self.gamma*(1 - done.float())*future_val 

                loss = loss_fn(q_taken, target)

                if step >= self.learning_start: 
                    # update model parameters  
                    optimizer.zero_grad()
                    loss.backward() 
                    optimizer.step()
                    if step % self.target_updates == 0:  
                        self.targetnet.load_state_dict(self.qnet.state_dict())

            step += 1 
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            if done: 
                obs, info = self.env.reset() 