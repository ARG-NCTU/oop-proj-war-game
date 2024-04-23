import pygame
import time

from math import atan2, cos, sin, pi, sqrt
from typing import Tuple


# from visualizer.collection import Collection
from visualizer.timer import Timer


TAU = 2 * pi


def distance(source, target):
    return sqrt((source[0] - target[0])**2 + (source[1] - target[1])**2)


# class Laser:
#     COLOR = pygame.Color("Yellow")

#     def __init__(self, source: Tuple[int, int], target: Tuple[int, int],
#                  turn_length: float):
#         self.source = source

#         self.timer = Timer(turn_length / 2)
#         self.dist = distance(source, target)
#         self.angle = atan2(target[1] - source[1], target[0] - source[0])

#     def draw(self, window):
#         delta = self.timer.get_delta()
#         full_rot = TAU / 60

#         min_angle = self.angle - full_rot / 2
#         angle = min_angle + full_rot * delta

#         dx = self.dist * cos(angle)
#         dy = self.dist * sin(angle)

#         target_pos = (
#             self.source[0] + dx,
#             self.source[1] + dy
#         )

#         pygame.draw.line(window, self.COLOR, self.source, target_pos)


# class Lasers(Collection):
#     class_type = Laser

#     def draw(self, window):
#         for p in self.all[:]:
#             p.draw(window)
#             if p.timer.is_done():
#                 self.all.remove(p)
                
                   
class LaserSprite(pygame.sprite.Sprite):
    COLOR = pygame.Color("Yellow")

    def __init__(self, source: Tuple[int, int], target: Tuple[int, int],
                 turn_length: float):
        super().__init__()
        self.source = source

        self.timer = Timer(turn_length / 2)
        self.dist = distance(source, target)
        self.angle = atan2(target[1] - source[1], target[0] - source[0])

    def update(self, window):
        delta = self.timer.get_delta()
        full_rot = TAU / 60

        min_angle = self.angle - full_rot / 2
        angle = min_angle + full_rot * delta

        dx = self.dist * cos(angle)
        dy = self.dist * sin(angle)

        target_pos = (
            self.source[0] + dx,
            self.source[1] + dy
        )

        pygame.draw.line(window, self.COLOR, self.source, target_pos)
        
        if self.timer.is_done():
            self.kill()
