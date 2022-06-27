"""
Convert RawLevel to pymunk space for physics simulation.
"""
from .raw_level import RawLevel
import pymunk


class PymunkLevel:
    def __init__(self, level: RawLevel):
        self.raw_level = level
        self.space = pymunk.Space()

    def populate_space(self):
        pass
