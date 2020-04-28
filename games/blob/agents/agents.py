from collections import deque
import numpy as np
from games.blob.agents.models import Simple_Blob_model, ReplayMemory
import time
import torch
import math



class DQN_agent:
    def __init__(self, world_size):
        self.policy_net = Simple_Blob_model(world_size)
        self.target_net = Simple_Blob_model(world_size)
        self.replay_memory = ReplayMemory(100_000)
        self.world_size = world_size
        self.discount = 0.999
        self.eps_start = 0.5
        self.eps_end = 0.95
        self.eps_decay = 100000
        self.eps = 0
        self.loss = 0
        self.optimizer = torch.optim.Adam(self.policy_net.parameters(), lr=0.001)


    def get_action(self, state, steps):
        self.eps = (self.eps_end + (self.eps_start - self.eps_end) * math.exp(-1*steps/self.eps_decay))

        if np.random.random() > self.eps:
            return np.random.randint(0, 4)

        return self.predict(state)

    def predict(self, state):
        state = state.reshape(1, 1, self.world_size[0], self.world_size[1])
        state = torch.from_numpy(state)
        state = state.float()
        state = state.cuda()

        predictions = self.policy_net(state)
        index = np.array(predictions.data.cpu()).argmax()

        return index

    def store_transition(self, state, action, new_state, reward):
        log = np.array([state, action, new_state, reward])
        return self.replay_memory.push(log)

    def learn(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def train(self):

        states, actions, new_states, rewards = np.array(self.replay_memory.sample(32))

        predicted_values = self.policy_net(states) # prendre la valeur de l'action choisie
        states_actions_values = predicted_values.gather(1, actions)

        next_state_values = self.target_net(new_states).max(1)[0].detach()
        expected_state_action_values = [(self.discount*value)+rewards[indexe] for indexe, value in enumerate(next_state_values)]

        expected_state_action_values = torch.tensor(expected_state_action_values).cuda()

        #calculer la loss
        loss = torch.nn.functional.smooth_l1_loss(states_actions_values, expected_state_action_values.unsqueeze(1))
        self.loss = loss.item()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


