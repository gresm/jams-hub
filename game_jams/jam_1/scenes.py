from __future__ import annotations

from ..engine import BaseScene
from .levels import listed_levels
from . import assets, color_permutations

from typing import Callable

import pygame as pg


class BaseGameScene(BaseScene):
    upper_scene: BaseScene | None
    page_name: str

    def init(self):
        pg.display.set_caption(f"Top and Bottom - {self.page_name}")

    def on_redirect_from(self, scene: BaseScene):
        self.upper_scene = scene

    def on_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if self.upper_scene:
                    self.manager.set_active_scene(self.upper_scene)
                else:
                    self.manager.game.stop()


class SceneWithBackground(BaseGameScene):
    color_iter: Callable[[], tuple[int, int, int]]

    def init(self):
        super().init()
        self.color_iter = color_permutations.color_iter()

    def update(self):
        super().update()
        if self.frame_counter.seconds % 5 == 0 and self.frame_counter.new_second:
            self.color_iter = color_permutations.color_iter()


class MainMenu(SceneWithBackground):
    def init(self):
        self.page_name = "Main Menu"
        super().init()

    def update(self):
        super().update()
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.manager.spawn_scene(LevelSelectionScene)

    def draw(self, surface: pg.Surface):
        surface.fill(self.color_iter())
        surface.blit(assets.font_title.render("Main Menu", True, (255, 255, 255)), (10, 10))
        surface.blit(assets.font_text.render("Press Enter to start", True, (255, 255, 255)), (10, 50))
        surface.blit(assets.font_text.render("Press Escape to quit", True, (255, 255, 255)), (10, 80))


class LevelSelectionScene(SceneWithBackground):
    selected_world: int
    selected_level: int
    selecting_level: bool

    def init(self):
        self.page_name = "Level Selection"
        self.selected_world = 1
        self.selected_level = 1
        self.selecting_level = True
        super().init()

    def update(self):
        super().update()
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                pass

    def draw(self, surface: pg.Surface):
        surface.fill(self.color_iter())
        surface.blit(assets.font_title.render("Level Selection", True, (255, 255, 255)), (10, 10))

        for num, level in listed_levels.items():
            if num == self.selected_world:
                lv_rect = pg.draw.rect(surface, (255, 255, 255), (10 + (num - 1) * 45, 50, 40, 40), 5)
            else:
                lv_rect = pg.draw.rect(surface, (255, 255, 255), (10 + (num - 1) * 45, 50, 40, 40), 3)
            text = assets.font_text.render(str(num), True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = lv_rect.center
            surface.blit(text, text_rect)

        if self.selecting_level:
            world = listed_levels[self.selected_world]

            for num, level in world.items():
                if num == self.selected_level:
                    lv_rect = pg.draw.rect(surface, (255, 255, 255), (40 + (num - 1) * 45, 100, 40, 40), 5)
                else:
                    lv_rect = pg.draw.rect(surface, (255, 255, 255), (40 + (num - 1) * 45, 100, 40, 40), 3)
                text = assets.font_text.render(str(num), True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = lv_rect.center
                surface.blit(text, text_rect)


class GameScene(SceneWithBackground):
    def init(self):
        self.page_name = "Game"
        super().init()

    def update(self):
        super().update()
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                pass

    def draw(self, surface: pg.Surface):
        surface.fill(self.color_iter())

    def on_redirect_from(self, scene: BaseScene):
        self.upper_scene = scene
