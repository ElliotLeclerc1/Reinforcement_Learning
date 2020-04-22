from commun.environement import Shapes
import pygame

white = (255, 255, 255)
black = (0, 0, 0)


class Food(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.color = (0, 0, 255)

    def render(self, display):
        pygame.draw.polygon(display, self.color, self.corners)


class Wall(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.color = black

    def render(self, display):
        pygame.draw.polygon(display, self.color, self.corners)


class Player(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.color = (0, 255, 0)
        self.speed = 5

    def move(self, displacement):
        super().move(displacement)

    def make_action(self, action):
        if action == 0:
            self.move((-1*self.speed, 0))
        elif action == 1:
            self.move((1*self.speed, 0))
        elif action == 2:
            self.move((0, -1*self.speed))
        elif action == 3:
            self.move((0, 1*self.speed))

    def render(self, display):
        pygame.draw.polygon(display, self.color, self.corners)
