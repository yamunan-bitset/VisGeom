from random import choice

import pygame
from enum import Enum


class Shape(Enum):
    IDLE = 0
    POINT = 1
    LINE = 2
    CIRCLE = 3


class Occupied:
    def __init__(self):
        self.occ_pts = list()

    def add_point(self, point):
        self.occ_pts.append(point)

    def if_is_occupied(self, point, depth=None):
        match depth:
            case None:
                return point in self.occ_pts
            case 1:
                if self.occ_pts[-1] == point:
                    return True
            case 2:
                if self.occ_pts[-2] == point or self.occ_pts[-1] == point:
                    return True
            case 3:
                if self.occ_pts[-3] == point or self.occ_pts[-2] == point or self.occ_pts[-1] == point:
                    return True
        return False

    def in_vicinity(self, pos):
        close_points = list()
        for point in self.occ_pts:
            if 0 <= abs(pos[0] - point[0]) <= 10 and 0 <= abs(pos[1] - point[1]) <= 10:
                close_points.append(point)
        if len(close_points) != 0:
            return choice(close_points)
        return None


class Point:
    def __init__(self, screen, pos, connection=0):
        self.screen = screen
        self.pos = pos
        match connection:
            case 0:
                self.c = (70, 70, 170)
            case 1:
                self.c = (50, 200, 50)
            case 2:
                self.c = (160, 60, 190)
            case 3:
                self.c = (190, 190, 20)
            case 4:
                self.c = (150, 150, 150)

    def draw(self):
        pygame.draw.circle(self.screen, self.c, self.pos, 10)


class Line:
    def __init__(self, screen, pos_1, pos_2):
        self.screen = screen
        self.pos = (pos_1, pos_2)
        try:
            self.m = (pos_1[1] - pos_2[1]) / (pos_1[0] - pos_2[0])
            self.c = pos_1[1] - self.m * pos_1[0]
        except ZeroDivisionError:
            self.m = 0

    def draw(self):
        Point(self.screen, self.pos[0], connection=1).draw()
        Point(self.screen, self.pos[1], connection=1).draw()
        pygame.draw.line(self.screen, (255, 0, 100), self.pos[0], self.pos[1])


def define_circle(pos):
    (a, b, c) = pos
    temp = b[0] ** 2 + b[1] ** 2
    bc = (a[0] ** 2 + a[1] ** 2 - temp) / 2
    cd = (temp - c[0] ** 2 - c[1] ** 2) / 2
    det = (a[0] - b[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (a[1] - b[1])

    if abs(det) == 0:
        return None, None

    # Center of circle
    cx = (bc * (b[1] - c[1]) - cd * (a[1] - b[1])) / det
    cy = ((a[0] - b[0]) * cd - (b[0] - c[0]) * bc) / det

    radius = ((cx - a[0]) ** 2 + (cy - a[1]) ** 2) ** (1 / 2)
    return (int(cx), int(cy)), int(radius)


class Circle:
    def __init__(self, screen, pos_1, pos_2, pos_3):
        self.screen = screen
        self.pos = (pos_1, pos_2, pos_3)
        self.c, self.r = define_circle(self.pos)

    def draw(self):
        Point(self.screen, self.pos[0], connection=1).draw()
        Point(self.screen, self.pos[1], connection=1).draw()
        Point(self.screen, self.pos[2], connection=1).draw()
        Point(self.screen, self.c, connection=4).draw()
        pygame.draw.circle(self.screen, (200, 90, 90), self.c, self.r, 3)
