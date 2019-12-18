import pygame
import sys
from rendering.Window import Window
from environement.Environement import Environement1
from agents.agents import Simple_perfect_agent, DQN_agent

white = (255, 255, 255)
black = (0, 0, 0)


class Game:
    def __init__(self):
        self.running = True
        self.game_count = 0
        self.max_game = 1000
        self.step_count = 0
        self.max_step = 500
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

        if self.render:
            pygame.quit()

        sys.exit()

    def new_game(self):
        print(self.game_count)
        self.render = self.game_count%100 == 0
        #self.agent = Simple_perfect_agent()
        #self.agent = Q_learning_agent()
        #self.agent.reward = 0
        self.step_count = 0
        self.environement = Environement1()

    def game_over(self):
        return len(self.environement.foods) == 0

    def step(self):

        state = self.environement.state
        action = self.agent.get_action(state)

        self.environement.turn(action)

        self.agent.new_state = self.environement.state
        self.agent.reward = self.environement.reward

        if not self.game_over():
            self.agent.learn()
        elif(self.agent.new_state[0] == 0 and self.agent.new_state[1] == 0):
            print("win")
            self.agent.win()

        self.step_count += 1




if __name__ == '__main__':

    game = Game()
    game.render = True
    game.play()
