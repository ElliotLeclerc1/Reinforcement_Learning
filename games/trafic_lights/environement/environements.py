from games.trafic_lights.environement.props import Intersection, Sides_info, Direction

Top_lane_info = Sides_info(1, 1, 1, 3, Direction.TOP)
Right_lane_info = Sides_info(1, 1, 1, 3, Direction.RIGHT)
Bot_lane_info = Sides_info(1, 1, 1, 3, Direction.BOT)
Left_lane_info = Sides_info(1, 1, 1, 3, Direction.LEFT)



class SingleLight_Environement:
    def __init__(self):
        self.world_size = (400, 400)
        self.interpreter = None
        self.intersection = Intersection(self.world_size[0]/2, self.world_size[1]/2, [Top_lane_info, Right_lane_info, Bot_lane_info, Left_lane_info])

    def get_state(self):
        return None

    def get_reward(self):
        return None

    def turn(self, action):
        pass
