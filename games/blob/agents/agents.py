from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque
import tensorflow as tf
import numpy as np
import time

# Own Tensorboard class

class DQN_agent:
    def __init__(self):
        self.model_name = "256x2"
        self.replay_memory_size = 50_000

        #main model train every set
        self.model = self.creat_model()

        #target model get predict every step
        self.target_model = self.creat_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=self.replay_memory_size)

        #self.tensorboard = ModifiedTensorBoard(log_dir="logs/{}-{}".format(self.model_name, int(time.time())))

        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0

    def get_action(self, state):
        epsilon = 0
        if epsilon > 1:
            return self.predict(state)

        random_action = "something"
        return random_action

    def predict(self, state):
        return self.target_model.predict(np.array(state).reshape(-1, *state.shape))[0]

    def store_transition(self, new_action, reward):
        #Todo "stuf"
        return NotImplemented

    def calculate_loss(self):
        return NotImplemented

    def gradient_descent(self):
        return NotImplemented

    def update_model(self):
        return NotImplemented


    def creat_model(self):
        model = Sequential()

        env_OBSERVATION_SPACE_VALUES = 12 #position et dimention de chaque objet
        env_ACTION_SPACE_SIZE = 4

        model.add(Conv2D(256, (3, 3), input_shape=env_OBSERVATION_SPACE_VALUES))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Conv2D(256, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        model.add(Dense(64))

        model.add(Dense(env_ACTION_SPACE_SIZE, activation='linear'))  # ACTION_SPACE_SIZE = how many choices (4)
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)
