import numpy as np

class Simple_perfect_agent:
    def __init__(self):
        self.state = None
        self.reward = 0

    def set_state(self, state):
        self.state = state

    def set_reward(self, reward):
        self.reward += reward

    def get_action(self):
        action = ""
        if self.state[0] > 0:
            action = "moveRight"
        if self.state[0] < 0:
            action = "moveLeft"
        if self.state[1] < 0:
            action = "moveUp"
        if self.state[1] > 0:
            action = "moveDown"

        return action


class DQN_agent:
    def __init__(self):
        self.new_state = None
        self.state = None
        self.reward = 0
        self.action = None
        #4 donnée de state avec 3 valeures possible et 4 actions possible
        self.q_table = np.random.uniform(low=-80, high=110, size=(3, 3, 3, 3, 4))

        self.learning_rate = 0.1
        self.discount = 0.95

    def get_action(self, state):
        self.state = state
        self.action = np.argmax(self.q_table[self.state[0], self.state[1], self.state[2], self.state[3]])
        return self.action

    def win(self):
        self.q_table[self.state[0], self.state[1], self.state[2], self.state[3], self.action] = 0

    def learn(self):
        max_futur_q = np.max(self.q_table[self.new_state[0], self.new_state[1], self.new_state[2], self.new_state[3]])
        current_q = self.q_table[self.state[0], self.state[1], self.state[2], self.state[3], self.action]

        new_q = (1-self.learning_rate)*current_q + self.learning_rate*(self.reward + self.discount*max_futur_q)
        self.q_table[self.state[0], self.state[1], self.state[2], self.state[3], self.action] = new_q
