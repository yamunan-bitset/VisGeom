import numpy as np
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


class Point:
    def __init__(self, screen, pos, connection=False):
        self.screen = screen
        self.pos = pos
        if connection:
            self.c = (50, 50, 50)
        else:
            self.c = (0, 0, 255)

    def draw(self):
        pygame.draw.circle(self.screen, self.c, self.pos, 10)


class Line:
    def __init__(self, screen, pos_1, pos_2):
        self.screen = screen
        self.pos = (pos_1, pos_2)

    def draw(self):
        Point(self.screen, self.pos[0], connection=True).draw()
        Point(self.screen, self.pos[1], connection=True).draw()
        pygame.draw.line(self.screen, (255, 0, 100), self.pos[0], self.pos[1])


def define_circle(pos):
    (a, b, c) = pos
    temp = b[0] ** 2 + b[1] ** 2
    bc = (a[0] ** 2 + a[1] ** 2 - temp) / 2
    cd = (temp - c[0] ** 2 - c[1] ** 2) / 2
    det = (a[0] - b[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (a[1] - b[1])

    if abs(det) == 0:
        return None, np.inf

    # Center of circle
    cx = (bc * (b[1] - c[1]) - cd * (a[1] - b[1])) / det
    cy = ((a[0] - b[0]) * cd - (b[0] - c[0]) * bc) / det

    radius = np.sqrt((cx - a[0]) ** 2 + (cy - a[1]) ** 2)
    return (int(cx), int(cy)), int(radius)


class Circle:
    def __init__(self, screen, pos_1, pos_2, pos_3):
        self.screen = screen
        self.pos = (pos_1, pos_2, pos_3)

    def draw(self):
        Point(self.screen, self.pos[0], connection=True).draw()
        Point(self.screen, self.pos[1], connection=True).draw()
        Point(self.screen, self.pos[2], connection=True).draw()
        c, r = define_circle(self.pos)
        pygame.draw.circle(self.screen, (0, 0, 255), c, r, 3)
