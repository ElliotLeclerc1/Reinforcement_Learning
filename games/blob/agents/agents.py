from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque
import tensorflow as tf
import numpy as np
import time

# Own Tensorboard class
class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = tf.summary.FileWriter(self.log_dir)

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)


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

        self.tensorboard = ModifiedTensorBoard(log_dir="logs/{}-{}".format(self.model_name, int(time.time())))

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

    def calculate_loss(self):

    def gradient_descent(self):

    def update_model(self):


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
