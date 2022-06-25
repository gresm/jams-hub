from __future__ import annotations

from ..engine import BaseScene
from . import assets, color_permutations

from typing import Callable

import pygame as pg


class MainMenu(BaseScene):
    frame_counter: int
    seconds_counter: int
    color_iter: Callable[[], tuple[int, int, int]]

    def init(self):
        pg.display.set_caption("Top and Bottom - Main Menu")
        self.color_iter = color_permutations.color_iter()
        self.frame_counter = 0
        self.seconds_counter = 0

    def update(self):
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.manager.spawn_scene(GameScene)
                elif event.key == pg.K_ESCAPE:
                    self.manager.game.stop()
        self.frame_counter += 1
        if self.frame_counter == 60:
            self.frame_counter = 0
            self.seconds_counter += 1
            if self.seconds_counter % 5 == 0:
                self.color_iter = color_permutations.color_iter()

    def draw(self, surface: pg.Surface):
        surface.fill(self.color_iter())
        surface.blit(assets.font_title.render("Main Menu", True, (255, 255, 255)), (10, 10))
        surface.blit(assets.font_text.render("Press Enter to start", True, (255, 255, 255)), (10, 50))
        surface.blit(assets.font_text.render("Press Escape to quit", True, (255, 255, 255)), (10, 80))


class GameScene(BaseScene):
    frame_counter: int
    seconds_counter: int
    upper_scene: BaseScene | None

    def init(self):
        pg.display.set_caption("Top and Bottom - Game")
        self.frame_counter = 0
        self.seconds_counter = 0
        self.upper_scene = None

    def update(self):
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.upper_scene:
                        self.manager.set_active_scene(self.upper_scene)
                    else:
                        self.manager.game.stop()

        self.frame_counter += 1
        if self.frame_counter == 60:
            self.frame_counter = 0
            self.seconds_counter += 1

    def draw(self, surface: pg.Surface):
        pass

    def on_redirect_from(self, scene: BaseScene):
        self.upper_scene = scene
