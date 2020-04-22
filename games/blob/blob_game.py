from games.blob.environement.Environement import Simple_blob_environement
from games.blob.agents.agents import DQN_agent
from rendering.Window import Window
import time
import pygame
import sys

grey = (200, 200, 200)
black = (0, 0, 0)


class Game:
    def __init__(self):
        self.running = True
        self.game_count = 0
        self.cumul_reward = 0
        self.max_game = 100
        self.step_count = 0
        self.max_step = 400
        self.render = True
        self.environement = Simple_blob_environement()
        self.agent = DQN_agent(self.environement.world_size)
        self.start_time = time.time()


    def play(self):
        if self.render:
            self.window = Window(grey, self.environement.world_size)

        self.playing()

    def playing(self):
        while self.running and self.game_count <= self.max_game:

            if self.game_over() or self.step_count >= self.max_step:
                print(f"game {self.game_count} over, {self.step_count} steps, reward {self.cumul_reward}, temps: {time.time() - self.start_time}")
                self.new_game()
                self.game_count += 1
            else:
                self.step()

            if self.render:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False

                props = [self.environement.player] + self.environement.walls + self.environement.foods
                self.window.render(props)

        sys.exit()

    def new_game(self):
        self.render = (self.game_count%20 == 0)
        self.agent = DQN_agent(self.environement.world_size)
        self.step_count = 0
        self.cumul_reward = 0
        self.start_time = time.time()
        self.environement = Simple_blob_environement()

    def game_over(self):
        return self.environement.game_over()

    def step(self):
        state = self.environement.get_state()
        action = self.agent.get_action(state)

        self.environement.turn(action)

        new_state = self.environement.get_state()

        self.cumul_reward += self.environement.get_reward()
        self.agent.store_transition(state, action, new_state, self.cumul_reward)

        #learn
        if (self.step_count >= 100 or self.game_count > 0) and self.step_count %10 == 0:
            self.agent.train()

        #copy both networks
        if self.step_count % 100 == 0:
            self.agent.learn()

        self.step_count += 1

