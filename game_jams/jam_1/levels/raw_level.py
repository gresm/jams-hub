"""
Loader for raw level data.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from enum import Enum


class Tile(Enum):
    ground = 0
    wall = 1
    player = 2
    goal = 3
    movable = 4
    moving_platform = 5


class Level:
    def __init__(self, upper_board: list[list[Tile]], lower_board: list[list[Tile]]):
        self.upper_board = upper_board
        self.lower_board = lower_board

    @classmethod
    def parse_raw(cls, upper: list[list[str]], lower: list[list[str]]) -> Level:
        upper_board = [[Tile(int(tile)) for tile in row] for row in upper]
        lower_board = [[Tile(int(tile)) for tile in row] for row in lower]
        return cls(upper_board, lower_board)


level_file_name_format = r"level_\d_\d\.csv"


def list_levels():
    """
    Returns a list of all levels in the "levels" directory.
    It does not load them from files, just lists them
    """
    levels_dir = Path(__file__).parent / "levels"
    ret: dict[int, dict[int, str]] = {}
    for file in levels_dir.iterdir():
        # check if file is a level file using regex
        if re.match(level_file_name_format, file.name):
            # get both numbers from file name using regex
            level_nums = re.findall(r"\d+", file.name)
            level_world = int(level_nums[0])
            level_num = int(level_nums[1])
            print(f"Found level {level_world}-{level_num}")
