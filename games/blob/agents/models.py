import torch.nn as nn
import torch
import random
import numpy as np
from torch.nn import functional, Linear

Log_index = ("state", "action", "next_state", "reward")


class ReplayMemory():
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def len(self):
        return len(self.memory)

    def push(self, log):
        if len(self.memory) > self.capacity:
            self.memory.pop(0)
        self.memory.append(log)

    def sample(self, batch_size):
        sample = np.array(random.choices(self.memory, k=batch_size))

        states = sample[:, 0]
        states = [state.tolist() for state in states]
        states = torch.tensor(states).cuda().unsqueeze(1)

        new_states = sample[:, 2]
        new_states = [new_state.tolist() for new_state in new_states]
        new_states = torch.tensor(new_states).cuda().unsqueeze(1)

        actions = list(sample[:, 1])
        actions = torch.tensor(actions)
        actions = actions.cuda().unsqueeze(1)

        rewards = sample[:, 3]

        return states, actions, new_states, rewards


class Simple_Blob_model(nn.Module):
    def __init__(self, input_size):
        super(Simple_Blob_model, self).__init__()
        self.conv1 = nn.Conv2d(1, 8, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=5, padding=2)
        self.conv3 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.pool3 = nn.MaxPool2d(2, 2)
        self.pool4 = nn.MaxPool2d(2, 2)
        self.bn1 = nn.BatchNorm2d(8)
        self.bn2 = nn.BatchNorm2d(16)
        self.bn3 = nn.BatchNorm2d(32)
        self.bn4 = nn.BatchNorm2d(64)
        self.fc1 = nn.Linear(int(64*input_size[0]/16*input_size[1]/16), int(64*input_size[0]/16*input_size[1]/16/2))
        self.fc2 = nn.Linear(int(64*input_size[0]/16*input_size[1]/16/2), 4)
        self.float()
        self.cuda()
        self.input_size = input_size

    def forward(self, x):
        out = nn.functional.relu(self.bn1(self.pool1(self.conv1(x))))
        out = nn.functional.relu(self.bn2(self.pool2(self.conv2(out))))
        out = nn.functional.relu(self.bn3(self.pool3(self.conv3(out))))
        out = nn.functional.relu(self.bn4(self.pool4(self.conv4(out))))
        out = out.view(-1, int(64*self.input_size[0]/16*self.input_size[1]/16))
        out = nn.functional.relu(self.fc1(out))
        out = nn.functional.softmax(self.fc2(out))

        return out



