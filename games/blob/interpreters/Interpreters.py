from skimage.draw import polygon
import numpy as np

class Interpretor1:
    def __init__(self):
        self.state = None
        self.win_reward = 25
        self.step_away_reward = -1
        self.step_foward_reward = 1

    def get_state(self, player, foods, walls, world_size):


        state = np.zeros(world_size)
        row_player, col_player = polygon(np.array(player.corners)[:, 1], np.array(player.corners)[:, 0])

        state[row_player, col_player] = 1

        for food in foods:
            row_food, col_food = polygon(np.array(food.corners)[:, 1], np.array(food.corners)[:, 0])
            state[row_food, col_food] = 2

        for wall in walls:
            row_wall, col_wall = polygon(np.array(wall.corners)[:, 1], np.array(wall.corners)[:, 0])
            state[row_wall, col_wall] = 3

        self.state = state
        return state



    def get_reward(self, foods):

        reward = -1

        if len(foods) == 0:
            reward = 25

        return reward
