from __future__ import annotations

from ..engine import BaseScene
from . import assets, color_permutations

from typing import Callable

import pygame as pg


class MainMenu(BaseScene):
    color_iter: Callable[[], tuple[int, int, int]]

    def init(self):
        pg.display.set_caption("Top and Bottom - Main Menu")
        self.color_iter = color_permutations.color_iter()

    def update(self):
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.manager.spawn_scene(LevelSelectionScene)
                elif event.key == pg.K_ESCAPE:
                    self.manager.game.stop()

        if self.frame_counter.seconds % 5 == 0 and self.frame_counter.new_second:
            self.color_iter = color_permutations.color_iter()

    def draw(self, surface: pg.Surface):
        surface.fill(self.color_iter())
        surface.blit(assets.font_title.render("Main Menu", True, (255, 255, 255)), (10, 10))
        surface.blit(assets.font_text.render("Press Enter to start", True, (255, 255, 255)), (10, 50))
        surface.blit(assets.font_text.render("Press Escape to quit", True, (255, 255, 255)), (10, 80))


class LevelSelectionScene(BaseScene):
    def init(self):
        pg.display.set_caption("Top and Bottom - Level Selection")

    def update(self):
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                pass


class GameScene(BaseScene):
    upper_scene: BaseScene | None
    background_color_iter: Callable[[], tuple[int, int, int]]

    def init(self):
        pg.display.set_caption("Top and Bottom - Game")
        self.upper_scene = None
        self.background_color_iter = color_permutations.color_iter()

    def update(self):
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.upper_scene:
                        self.manager.set_active_scene(self.upper_scene)
                    else:
                        self.manager.game.stop()

        if self.frame_counter.seconds % 5 == 0 and self.frame_counter.new_second:
            self.background_color_iter = color_permutations.color_iter()

    def draw(self, surface: pg.Surface):
        surface.fill(self.background_color_iter())

    def on_redirect_from(self, scene: BaseScene):
        self.upper_scene = scene
