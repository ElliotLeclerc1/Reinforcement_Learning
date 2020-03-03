from games.blob.environement.Environement import Environement1
from games.blob.agents.agents import DQN_agent
from rendering.Window import Window
import pygame
import sys

white = (255, 255, 255)
black = (0, 0, 0)


class Game:
    def __init__(self):
        self.running = True
        self.game_count = 0
        self.max_game = 500
        self.step_count = 0
        self.max_step = 1500
        self.render = True
        self.agent = DQN_agent()
        self.environement = Environement1()

    def play(self):
        if self.render:
            self.window = Window(white, self.environement.world_size)

        self.playing()

    def playing(self):
        while self.running and self.game_count <= self.max_game:

            if self.game_over() or self.step_count >= self.max_step:
                print("game over")
                self.new_game()
                self.game_count += 0
            else:
                self.step()

            if self.render:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False

                props = [self.environement.player] + self.environement.walls + self.environement.foods
                self.window.render(props)

        if self.render:
            pygame.quit()

        sys.exit()

    def new_game(self):
        print(self.game_count)
        self.render = self.game_count%100 == 0
        self.agent = DQN_agent()
        #self.agent.reward = 0
        self.step_count = 0
        self.environement = Environement1()

    def game_over(self):
        return self.environement.game_over()

    def step(self):

        state = self.environement.get_state()
        action = self.agent.get_action(state)

        self.environement.turn(action)

        new_state = self.environement.get_state()
        reward = self.environement.get_reward()

        self.agent.store_transition(state, action, new_state, reward)
        print(self.agent.replay_memory.len())

        self.step_count += 1
