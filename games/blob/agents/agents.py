from collections import deque
import numpy as np
from games.blob.agents.models import Simple_Blob_model, ReplayMemory
import time
import torch



class DQN_agent:
    def __init__(self):
        self.prediction_model = Simple_Blob_model(300*300)
        self.learning_model = Simple_Blob_model(300*300)
        self.replay_memory = ReplayMemory(100_000)


    def get_action(self, state):
        epsilon = 0
        if epsilon > 1:
            return self.predict(state)

        random_action = "something"
        return 0

    def predict(self, state):
        state = torch.from_numpy(state)
        return 0
        #return self.prediction_model(*state)

    def store_transition(self, state, action, new_action, reward):
        #Todo "stuf"
        log = [state, action, new_action, reward]
        return self.replay_memory.push(log)

    def calculate_loss(self):
        return NotImplemented

    def gradient_descent(self):
        return NotImplemented

    def update_model(self):
        return NotImplemented


    def creat_model(self):
        pass

    def update_replay_memory(self, log):
        self.replay_memory.push(log)
