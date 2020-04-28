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
        self.max_game = 300
        self.max_step = 1000
        
        self.new_game()
        self.agent = DQN_agent(self.environement.world_size)

        


    def play(self):
        if self.render:
          self.window = Window(black, self.environement.world_size)

        self.playing()

    def playing(self):
        while self.running and self.game_count <= self.max_game:

            if self.game_over() or self.step_count >= self.max_step:
                self.stats[1] = self.agent.eps
                self.stats[3] = self.agent.loss
                print(f"game {self.game_count} over, {self.step_count} steps, reward {self.cumul_reward}, temps: {time.time() - self.start_time}")
                print(f"  start eps: {self.stats[0]}, end eps: {self.stats[1]}, start loss: {self.stats[2]}, mean loss: {self.stats[5]/self.step_count}")
                print(f"  {self.stats[4]}")
                self.new_game()
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
        self.game_count += 1
        self.render = (self.game_count%10 == 0) and self.game_count > 10
        self.environement = Simple_blob_environement()
        self.step_count = 0
        self.cumul_reward = 0
        self.start_time = time.time()
        self.stats = [0, 0, 0, 0, [], 0]

    def game_over(self):
        return self.environement.game_over()

    def step(self):
        state = self.environement.get_state()

        step_count = (self.game_count*self.max_step) + self.step_count
        action = self.agent.get_action(state, step_count)
        self.stats[4].append(action)

        self.environement.turn(action)

        new_state = self.environement.get_state()

        self.cumul_reward += self.environement.get_reward()
        self.agent.store_transition(state, action, new_state, self.cumul_reward)

        #learn
        #if (self.game_count > 1) and self.step_count %5 == 0:
        if (self.game_count > 10):
            self.agent.train()
            if self.step_count == 0:
              self.stats[0] = self.agent.eps
              self.stats[2] = self.agent.loss
            self.stats[5] += self.agent.loss

        #copy both networks
        if self.step_count % 450 == 0:
            self.agent.learn()

        self.step_count += 1

