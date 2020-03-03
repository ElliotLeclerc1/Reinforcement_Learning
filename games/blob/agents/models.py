import torch.nn as nn
import random
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
        return random.choices(self.memory, batch_size)


class Simple_Blob_model(nn.Module):
    def __init__(self, input_size):
        super(Simple_Blob_model, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.bn1 = nn.BatchNorm2d(16)
        self.bn2 = nn.BatchNorm2d(32)
        self.fc1 = nn.Linear(int(32*input_size/4), 4)

    def forward(self, x):
        out = nn.functional.relu(self.bn1(self.pool1(self.conv1(x))))
        out = nn.functional.relu(self.bn2(self.pool2(self.conv2(out))))
        out = nn.functional.softmax(self.fc1(out))

        return out



