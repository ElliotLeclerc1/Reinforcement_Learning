class Interpretor1:
    def __init__(self):
        self.state = None
        self.win_reward = 25
        self.step_away_reward = -1
        self.step_foward_reward = 1

    def get_state(self, player, foods, walls):

        #état représente la position [gauche[-1] - enligné[0] - droite[1], enbas[-1] - enligné[0] - audessus[1]] des objets et du joueur
        state = [1, 1, 1, 1]

        if len(foods) == 0:
            return state

        if player.x + player.width/2 < foods[0].x - foods[0].width/2:
            state[0] = 2
        if player.x - player.width/2 > foods[0].x + foods[0].width/2:
            state[0] = 0

        if player.y + player.height/2 < foods[0].y - foods[0].height/2:
            state[1] = 2
        if player.y - player.height/2 > foods[0].y + foods[0].height/2:
            state[1] = 0

        if player.x + player.width/2 < walls[0].x - walls[0].width/2:
            state[2] = 2
        if player.x - player.width/2 > walls[0].x + walls[0].width/2:
            state[2] = 0

        if player.y + player.height/2 < walls[0].y - walls[0].height/2:
            state[3] = 2
        if player.y - player.height/2 > walls[0].y + walls[0].height/2:
            state[3] = 0

        self.state = state
        return state



    def get_reward(self, foods):

        if len(foods) == 0:
            return self.win_reward

        reward = -2
        if self.state[0] == 1:
            reward += 1
        if self.state[1] == 1:
            reward += 1
        return reward
