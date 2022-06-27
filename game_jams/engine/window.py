from __future__ import annotations

from typing import Callable
from warnings import warn

import pygame as pg


pg.init()


class GameState:
    screen: pg.Surface

    def __init__(self, fps: int, screen_size: tuple[int, int]):
        self.max_fps = fps
        self.clock = pg.time.Clock()
        self.running = False
        self._frame: Callable[[pg.Surface, float], ...] | None = None
        self.size = screen_size

    def init(self):
        self.screen = pg.display.set_mode(self.size)
        self.running = True

    def stop(self):
        self.running = False

    def frame(self, func: Callable[[pg.Surface, float], ...]):
        self._frame = func
        return func

    def run(self):
        while self.running:
            if self._frame is not None:
                if max_fps != -1:
                    ms = self.clock.tick(max_fps)
                else:
                    ms = self.clock.tick()
                self._frame(self.screen, ms / 1000.0)  # maybe you are missing "window" and "delta_time" arguments
            else:
                warn("Running without specified frame executor")
                break


size = (800, 800)
max_fps = 60
game = None


def get_game(game_size: tuple[int, int] | None = None, fps: int | None = None):
    global game
    ret = GameState(fps or max_fps, game_size or size)
    game = ret
    return ret


__all__ = [
    "size",
    "max_fps",
    "get_game",
    "game",
    "GameState"
]
