"""
Convert RawLevel to pymunk space for physics simulation.
"""
from raw_level import RawLevel
from enum import Enum
import pymunk


class CollisionMasks(Enum):
    players = 1
    walls = 4
    goals = 8
    movable = 16
    level_boundary = 32
    movable_go_through_boundary = 64
    player_collide_with = 125  # walls | movable | goals | level_boundary | movable_go_through_boundary | players
    movable_collide_with = 53  # walls | movable | players | level_boundary


class PymunkLevel:
    def __init__(self, level: RawLevel):
        self.raw_level = level
        self.space = pymunk.Space()

    def populate_space(self):
        pass
