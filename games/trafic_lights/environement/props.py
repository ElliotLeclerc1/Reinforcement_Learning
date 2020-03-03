import pygame
from commun.environement import Shapes
from enum import Enum

Direction_vector = [(0, 1), (1, 0), (0, -1), (-1, 0)]
Angle = [90, 180, 270, 0]
lane_size = 12


class Direction(Enum):
    TOP = 0
    RIGHT = 1
    BOT = 2
    LEFT = 3


class Cars(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.color = (0, 0, 255)

    def render(self, display):
        pygame.draw.polygon(display, self.color, self.corners)


class Light(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.is_green = True

    def switch(self):
        self.is_green = not self.is_green


class Lane(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle, cars, direction_vector, light):
        super().__init__(x, y, width, height, angle)
        self.cars = cars
        self.direction_vector = direction_vector
        self.connections = []
        self.light = light
        self.color = (50, 50, 50)

    def add_conection(self, destination_lane):
        self.connections.append(destination_lane)

    def render(self, display):
        pygame.draw.polygon(display, self.color, self.corners)


class Sides_info:
    def __init__(self, nb_straight_lane_to_intersection, nb_of_left_turn_lanes, nb_of_right_turn_lanes, nb_of_lanes_from_intersection, direction):
        self.nb_straight_lane_to_intersection = nb_straight_lane_to_intersection
        self.nb_of_lanes_from_intersection = nb_of_lanes_from_intersection
        self.nb_of_left_turn_lanes = nb_of_left_turn_lanes
        self.nb_of_right_turn_lanes = nb_of_right_turn_lanes
        self.angle = Angle[direction.value]
        self.width = 100
        self.height = (nb_of_left_turn_lanes + nb_of_lanes_from_intersection + nb_of_right_turn_lanes + nb_straight_lane_to_intersection)*lane_size
        self.direction = direction


class Side(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle, direction, lanes):
        super().__init__(x, y, width, height, angle)
        self.direction = direction
        self.lanes = lanes
        self.color = (100, 100, 100)

    def render(self, display):
        pygame.draw.polygon(display, self.color, self.corners)
        for lane in self.lanes:
            lane.render(display)


class Intersection(Shapes.Rectangle):
    def __init__(self, x, y, sides_info):
        self.sides_info = sides_info
        self.side = self.get_dimentions()
        super().__init__(x, y, self.side, self.side, 0)
        self.sides = self.get_sides()
        self.color = (200, 200, 200)

    def get_dimentions(self):
        side = 0
        for side_info in self.sides_info:
            side = max(side, side_info.height)

        return side


    def get_sides(self):
        sides = []
        side_width = 100
        for side_info in self.sides_info:
            if side_info is not None:
                side_center_x = self.x + (self.side/2 + side_width/2)*Direction_vector[side_info.direction.value][0]
                side_center_y = self.y + (self.side/2 + side_width/2)*Direction_vector[side_info.direction.value][1]
                side = Side(side_center_x, side_center_y, side_width, side_info.height, side_info.angle, side_info.direction, self.get_lanes(side_info, (side_center_x, side_center_y)))
                sides.append(side)

        return sides

    def get_lanes(self, side_info, side_center):
        lanes = []

        #on ajoute les lanes de gauche a droite
        for i in range(side_info.nb_of_lanes_from_intersection):
            padding = 1
            direction = Direction_vector[side_info.direction.value] #todo corriger direction inversé
            x = side_center[0] - (side_info.height/2 - lane_size*len(lanes) - lane_size/2)*direction[1]
            y = side_center[1] + (side_info.height/2 - lane_size*len(lanes) - lane_size/2)*direction[0]
            height = lane_size - 2*padding
            width = side_info.width
            lane = Lane(x, y, width, height, side_info.angle, [], direction, None)
            lanes.append(lane)

        for i in range(side_info.nb_of_left_turn_lanes + side_info.nb_of_right_turn_lanes + side_info.nb_straight_lane_to_intersection):
            padding = 1
            direction = Direction_vector[side_info.direction.value]
            x = side_center[0] - (side_info.height/2 - lane_size*len(lanes) - lane_size/2)*direction[1]
            y = side_center[1] + (side_info.height/2 - lane_size*len(lanes) - lane_size/2)*direction[0]
            height = lane_size - 2*padding
            width = side_info.width
            lane = Lane(x, y, width, height, side_info.angle, [], direction, self.get_light())
            lanes.append(lane)

        return lanes

    def get_light(self):
        return None

    def render(self, display):
        pygame.draw.polygon(display, self.color, self.corners)

        for side in self.sides:
            side.render(display)

