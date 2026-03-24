import torch 
import torch.nn as nn 
import gymnasium as gym 
from gymnasium import spaces 
import random 
import numpy as np 
from torch.distributions import Categorical

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

        info = {}
        
        return obs, reward, terminated, truncated, info 

    def reset(self): 
        return 

    def _getobs(self): 
        obs = []
        return obs 

    def _getreward(self): 
        reward = 1 
        return reward
    

class FFNN(nn.Module): 
    def __init__(self, input_dim, d_model, output_dim, n_layers): 
        super().__init__()
        self.input_dim = input_dim
        self.d_model = d_model 
        self.output_dim = output_dim 
        self.n_layers = n_layers 
        self.input = nn.Linear(input_dim, output_dim)
        self.hidden = nn.ModuleList([])
        for _ in range(self.n_layers): 
            self.hidden.append(nn.Linear(d_model, d_model))
        self.output = nn.Linear(self.d_model, self.output_dim)

    def forward(self, x): 
        out = self.input(x)
        for _ in range(self.n_layers): 
            out = self.hidden(out)
        out = self.output(out)

        return out 
    

class PPO(nn.Module): 
    def __init__(self, 
                 env,
                 obs_dim, 
                 action_dim, 
                 d_model, 
                 n_layers, 
                 learning_rate,
                 n_steps, 
                 gamma, 
                 lamda, 
                 update_epochs, 
                 eps):  
        self.env = env   
        self.obs_dim = obs_dim 
        self.action_dim = action_dim 
        self.d_model = d_model 
        self.n_layers = n_layers 
        self.lr = learning_rate
        self.n_steps = n_steps 
        self.gamma = gamma
        self.lamda = lamda
        self.update_epochs = update_epochs
        self.eps = eps 

        self.actor = FFNN(self.obs_dim, self.d_model, self.action_dim, self.n_layers)
        self.critic = FFNN(self.obs_dim, self.d_model, self.action_dim, self.n_layers)

    def learn(self, max_timesteps): 
        obs, info = self.env.reset() 
        trajectories = []

        actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=self.lr)
        critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=self.lr)
        
        total_steps= 0 

        while total_steps < max_timesteps: 
            for _ in range(self.n_steps): 
                # collect trajectories 
                obs = torch.tensor(obs)
                action_logits = self.actor(obs)
                dist = Categorical(logits=action_logits)
                action = dist.sample() 
                log_prob = dist.log_prob(action)
                next_obs, reward, terminated, truncated, info = self.env.step(action.item())
                done = terminated or truncated
                value = self.critic(obs).squeeze()
                trajectories.append([obs, 
                                     action, 
                                     reward, 
                                     next_obs, 
                                     log_prob.detach(), 
                                     value.detach(), 
                                     done])
                
                if done: 
                    obs, info = self.env.reset() 
                else: 
                    obs = next_obs
                
                total_steps += 1 

            # compute the advantages 
            advantages = []
            deltas = []
            gae = 0 
            for t in range(len(trajectories), -1, -1): 
                value = trajectories[t][5]
                reward = trajectories[t][2]
                done = trajectories[t][6]
                if t == len(trajectories) - 1: 
                    next_value = 0 
                else: 
                    next_value = trajectories[t+1][5]

                delta = reward + self.gamma*(1-done)*next_value - value 

                gae = delta + self.gamma*self.lamda*(1-done)*gae
                advantages.insert(0, gae)
                deltas.insert(0, delta)


            # convert to tensors
            states = torch.stack([x[0] for x in trajectories])
            actions = torch.stack([x[1] for x in trajectories])
            old_log_probs = torch.stack([x[4] for x in trajectories]).detach()
            advantages = torch.stack(advantages).detach()
            returns = torch.stack(returns).detach()

            # normalize the advantages 
            advantages = (advantages - advantages.mean())/(advantages.std() + 1e-6)
            returns = advantages + trajectories[5]

            # update policy 
            for _ in range(self.update_epochs): 
                action_logits = self.actor(states)
                new_dist = Categorical(action_logits)
                new_action = new_dist.sample()
                new_log_prob = new_dist.log_prob(new_action)
                
                ratios = torch.exp(new_log_prob-old_log_probs)

                surr1 = ratios*advantages
                surr2 = torch.clamp(ratios, 1-self.eps, 1+self.eps)*advantages 

                actor_loss = -torch.min(surr1, surr2).mean()

                actor_optimizer.zero_grad()
                actor_loss.backward() 
                actor_optimizer.step()

                value_pred = self.critic(states)

                critic_loss = ((value_pred - returns)**2).mean()

                critic_optimizer.zero_grad() 
                critic_loss.backward() 
                critic_optimizer.step() 




                

            


            



