from games.blob.environement.Props import Player, Food, Wall
from commun.physics.ColisionDetection import rectangles_colision
from games.blob.interpreters.Interpreters import Perfect_info_interpretor
import numpy as np


class Environement:
    def __init__(self):
        self.world_size = (32, 32)
        self.player = Player(int(np.random.uniform(0, 1) * self.world_size[0]), int(np.random.uniform(0, 1) * self.world_size[1]), 10, 10, 0)
        self.foods = []
        self.walls = []
        self.step_away_reward = -1
        self.step_foward_reward = 1
        self.win_reward = 25
        self.interpreter = None

    def game_over(self):
        return len(self.foods) == 0

    def get_state(self):
        return self.interpreter.get_state(self.player, self.foods, self.walls, self.world_size)

    def get_reward(self):
        return self.interpreter.get_reward(self.foods)

    def turn(self, action):
        prev_position = (self.player.x, self.player.y)
        self.player.make_action(action)
        self.keep_in_world()

        for wall in self.walls:
            colide_wall = self.check_wall_colide(wall)

            if colide_wall:
                self.player.x = prev_position[0]
                self.player.y = prev_position[1]

        for food in self.foods:
            colide_food = rectangles_colision(self.player, food)

            if colide_food:
                self.foods = []

    def check_wall_colide(self, wall):
        return rectangles_colision(wall, self.player)

    def keep_in_world(self):
        if self.player.x + self.player.width >= self.world_size[0]:
            self.player.x = self.world_size[0] - self.player.width
        if self.player.y + self.player.height >= self.world_size[1]:
            self.player.y = self.world_size[1] - self.player.height
        if self.player.x - self.player.width <= 0:
            self.player.x = 0 + self.player.width
        if self.player.y - self.player.height <= 0:
            self.player.y = 0 + self.player.height


class Simple_blob_environement(Environement):
    def __init__(self):
        super().__init__()
        self.player = Player(10, 10, 2, 2, 0)

        food = Food(20, 20, 4, 4, 0)
        self.foods.append(food)

        self.interpreter = Perfect_info_interpretor()
        self.state = self.interpreter.get_state(self.player, self.foods, self.walls, self.world_size)
        self.reward = self.interpreter.get_reward(self.foods)






