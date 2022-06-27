"""
Loader for raw level data.
"""
from __future__ import annotations

import re
from functools import lru_cache, cache
from pathlib import Path
from enum import Enum


class Tile(Enum):
    air = 0
    wall = 1
    player = 2
    goal = 3
    movable = 4


class LevelInfo:
    def __init__(self, title: str, theme: str, width: int, height: int):
        self.title = title
        self.theme = theme
        self.width = width
        self.height = height


class RawLevel:
    def __init__(self, level_info: LevelInfo, upper_board: list[list[Tile]], lower_board: list[list[Tile]]):
        self.level_info = level_info
        self.upper_board = upper_board
        self.lower_board = lower_board

    @classmethod
    def parse_raw(cls, info: list[str], upper: list[list[str]], lower: list[list[str]]) -> RawLevel:
        level_info = LevelInfo(info[0], info[1], int(info[2]), int(info[3]) * 2)
        upper_board = [[Tile(int(tile)) for tile in row] for row in upper]
        lower_board = [[Tile(int(tile)) for tile in row] for row in lower]
        return cls(level_info, upper_board, lower_board)


level_file_name_format = r"level_\d_\d\.csv"


@lru_cache(maxsize=1)
def list_raw_levels():
    """
    Returns a list of all game_levels in the "game_levels" directory.
    It does not load them from files, just lists them
    """
    levels_dir = Path(__file__).parent / "game_levels"
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


def parse_text(text: str) -> list[list[str]]:
    """
    Parses a text file into a list of lists of strings.
    """
    lines = text.split("\n")
    ret = []
    for line in lines:
        ret.append(line.split(","))
    return ret


@cache
def load_level(level_world: int, level_num: int) -> RawLevel:
    """
    Loads a level from a file.
    """
    file = list_raw_levels()[level_world][level_num]
    with file.open() as f:
        extra_info = parse_text(f.readline())[0]
        text = f.read()
        boards = text.split("\n!\n")
        upper = parse_text(boards[0])
        lower = parse_text(boards[1])
    return RawLevel.parse_raw(extra_info, upper, lower)


@lru_cache(maxsize=1)
def list_levels() -> dict[int, dict[int, RawLevel]]:
    """
    Loads all levels from files and returns them as a dictionary.
    :return:
    """
    lst = list_raw_levels()
    ret = {}
    for world in lst:
        ret[world] = {}
        for level in lst[world]:
            ret[world][level] = load_level(world, level)
    return ret


__all__ = ["RawLevel", "Tile", "LevelInfo", "load_level", "list_levels"]
