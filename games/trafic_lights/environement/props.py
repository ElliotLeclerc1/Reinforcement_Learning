import pygame
from commun.environement import Shapes
from enum import Enum


class Directions(Enum):
    Top = 0
    Right = 1
    Bottom = 2
    Left = 3


class Light(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.is_green = True

    def switch(self):
        self.is_green = not self.is_green


class Cars(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.color = (0, 0, 255)

    def render(self, display):
        pygame.draw.polygon(display, self.color, self.corners)


class Lane(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle, cars, direction, light):
        super().__init__(x, y, width, height, angle)
        self.cars = cars
        self.direction = direction
        self.connections = []
        self.light = light

    def add_conection(self, destination_lane):
        self.connections.append(destination_lane)


class Side(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle, direction, lanes):
        super().__init__(x, y, width, height, angle)
        self.direction = direction
        self.lanes = lanes


class Intersection(Shapes.Rectangle):
    def __init__(self, x, y, width, height, angle, sides):
        super().__init__(x, y, width, height, angle)
        self.sides = sides

    def render(self, display):
        pass



class Simple_intersection(Intersection):
    def __init__(self, x, y, width, height, angle):
        sides = self.sides()
        super().__init__(x, y, width, height, angle, sides)

    def get_sides(self):
        sides = []
        for i in range(4):
            direction = Directions(i)
            lanes = self.get_lanes(direction)
            side = Side(direction, lanes)

            sides.append(side)

        return sides

    def get_lanes(self, side):
        lanes = []
        for i in range(2):
            cars = []
            lane = Lane(cars, side, Light())
            opposit_lane = Lane([], get_opposit_direction(side), None)

            lanes.append(opposit_lane)
            lanes.append(lane)

        return lanes



def get_opposit_direction(direction):
    if direction == Directions.Top:
        return Directions.Bottom
    if direction == Directions.Right:
        return Directions.Left
    if direction == Directions.Bottom:
        return Directions.Top
    if direction == Directions.Left:
        return Directions.Right

    return None

def get_next_direction(direction):
    if direction == Directions.Top:
        return Directions.Left
    if direction == Directions.Right:
        return Directions.Top
    if direction == Directions.Bottom:
        return Directions.Right
    if direction == Directions.Left:
        return Directions.Bottom

    return None
