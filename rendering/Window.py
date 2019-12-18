import pygame

class Window:
    def __init__(self, background, environement_size):
        self.background = background
        pygame.init()
        self.display = pygame.display.set_mode((environement_size[0], environement_size[1]))
        pygame.display.set_caption('RL AI')
        self.clock = pygame.time.Clock()

    def render(self, props):
        self.display.fill(self.background)

        for prop in props:
            prop.render(self.display)

        pygame.display.flip()
        self.clock.tick(120)
