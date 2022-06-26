"""
Loader for raw level data.
"""
from __future__ import annotations

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


class LevelInfo:
    def __init__(self, title: str, theme: str):
        self.title = title
        self.theme = theme


class RawLevel:
    def __init__(self, level_info: LevelInfo, upper_board: list[list[Tile]], lower_board: list[list[Tile]]):
        self.level_info = level_info
        self.upper_board = upper_board
        self.lower_board = lower_board

    @classmethod
    def parse_raw(cls, info: list[str], upper: list[list[str]], lower: list[list[str]]) -> RawLevel:
        level_info = LevelInfo(info[0], info[1])
        upper_board = [[Tile(int(tile)) for tile in row] for row in upper]
        lower_board = [[Tile(int(tile)) for tile in row] for row in lower]
        return cls(level_info, upper_board, lower_board)


level_file_name_format = r"level_\d_\d\.csv"


def list_levels():
    """
    Returns a list of all levels in the "levels" directory.
    It does not load them from files, just lists them
    """
    levels_dir = Path(__file__).parent / "levels"
    ret: dict[int, dict[int, Path]] = {}
    for file in levels_dir.iterdir():
        # check if file is a level file using regex
        if re.match(level_file_name_format, file.name):
            # get both numbers from file name using regex
            level_nums = re.findall(r"\d+", file.name)
            level_world = int(level_nums[0])
            level_num = int(level_nums[1])
            if level_world not in ret:
                ret[level_world] = {}

            ret[level_world][level_num] = file
    return ret


levels = list_levels()


def parse_text(text: str) -> list[list[str]]:
    """
    Parses a text file into a list of lists of strings.
    """
    lines = text.split("\n")
    ret = []
    for line in lines:
        ret.append(line.split(","))
    return ret


def load_level(level_world: int, level_num: int) -> RawLevel:
    """
    Loads a level from a file.
    """
    file = levels[level_world][level_num]
    with file.open() as f:
        extra_info = parse_text(f.readline())[0]
        text = f.read()
        boards = text.split("\n!\n")[0]
        upper = parse_text(boards[0])
        lower = parse_text(boards[1])
    return RawLevel.parse_raw(extra_info, upper, lower)
