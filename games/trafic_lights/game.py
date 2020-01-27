import pygame
import sys
from rendering.Window import Window

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
        self.agent = None
        self.environement = None

    def play(self):
        if self.render:
            self.window = Window(white, self.environement.world_size)

        self.playing()

    def playing(self):
        while self.running and self.game_count <= self.max_game:

            if self.game_over() or self.step_count >= self.max_step:
                print("game over")
                self.new_game()
                self.game_count += 1
            else:
                self.step()

            if self.render:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False

                #props = [self.environement.player] + self.environement.walls + self.environement.foods
                self.window.render(props)

        if self.render:
            pygame.quit()

        sys.exit()

    def new_game(self):
        print(self.game_count)
        self.render = self.game_count%100 == 0
        #self.agent = Simple_perfect_agent()
        #self.agent.reward = 0
        self.step_count = 0
        self.environement = None

    def game_over(self):
        return NotImplementedError

    def step(self):

        state = self.environement.get_state()
        action = self.agent.get_action(state)

        self.environement.turn(action)

        self.agent.new_state = self.environement.get_state()
        self.agent.reward = self.environement.get_reward()

        if not self.game_over():
            self.agent.learn()
        elif(self.agent.new_state[0] == 1 and self.agent.new_state[1] == 1):
            print("win")
            self.agent.win()

        self.step_count += 1