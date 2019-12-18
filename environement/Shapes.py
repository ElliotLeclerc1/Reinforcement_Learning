import numpy as np


class Rectangle:
    def __init__(self, x, y, width, height, angle):
        self.x = x
        self.y = y
        self. width = width
        self.height = height
        self.angle = angle
        self.calculate_corners()
        self.calculate_rectangle_separating_axis()

    def move(self, displacement):
        self.x += displacement[0]
        self.y += displacement[1]

        self.calculate_corners()
        self.calculate_rectangle_separating_axis()

    def calculate_rectangle_separating_axis(self):
        corners = self.corners
        vectors = []

        for i in range(len(self.corners)):
            p1 = corners[i]
            p2 = corners[0 if i + 1 == len(self.corners) else i + 1]
            vectors.append(p2 - p1)

        unit_vectors = [
            [vector[0] / np.sqrt(vector[0] ** 2 + vector[1] ** 2), vector[1] / np.sqrt(vector[0] ** 2 + vector[1] ** 2)]
            for vector in vectors]
        axis = [np.array([-unit_vector[1], unit_vector[0]]) for unit_vector in unit_vectors]

        self.separating_axis = axis

    def calculate_corners(self):
        points = [(self.width / 2, self.height / 2), (self.width / 2, -self.height / 2), (-self.width / 2, -self.height / 2),
                  (-self.width / 2, self.height / 2)]
        rectangle_corners = [self.rotate_point(point, self.angle) + [self.x, self.y] for point in points]

        self.corners = rectangle_corners

    # rotation dans le sens anti horraire height y, width x
    def rotate_point(self, coord, theta):
        rad = 2 * np.pi / 360 * theta
        rotation_matrix = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])
        point = np.array([coord[0], coord[1]])
        rotated_point = rotation_matrix.dot(point)

        return rotated_point
