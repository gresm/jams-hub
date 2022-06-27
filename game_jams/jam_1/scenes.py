from __future__ import annotations

from ..engine import BaseScene
from .levels import listed_levels, PymunkLevel
from .levels.raw_level import RawLevel
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
                    self.manager.set_active_scene(self.upper_scene, silent=True)
                else:
                    self.manager.game.stop()


class SceneWithBackground(BaseGameScene):
    color_iter: Callable[[], tuple[int, int, int]]

    def init(self):
        super().init()
        self.color_iter = color_permutations.color_iter()

    def update(self, delta_time: float):
        super().update(delta_time)
        if self.frame_counter.seconds % 5 == 0 and self.frame_counter.new_second:
            self.color_iter = color_permutations.color_iter()


class MainMenu(SceneWithBackground):
    def init(self):
        self.page_name = "Main Menu"
        super().init()

    def update(self, delta_time: float):
        super().update(delta_time)
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
        super().init()
        self.reset_selection()

    def reset_selection(self):
        self.selected_world = 1
        self.selected_level = 1
        self.selecting_level = False

    def update(self, delta_time: float):
        super().update(delta_time)
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                if event.key in {pg.K_w, pg.K_UP}:
                    self.selecting_level = False
                if event.key in {pg.K_s, pg.K_DOWN, pg.K_RETURN}:
                    if not self.selecting_level:
                        self.selecting_level = True
                    else:
                        self.manager.spawn_scene(GameScene)
                if event.key in {pg.K_a, pg.K_LEFT}:
                    if self.selecting_level:
                        self.selected_level -= 1
                        if self.selected_level not in listed_levels[self.selected_world]:
                            self.selected_level = max(listed_levels[self.selected_world])
                    else:
                        self.selected_world -= 1
                        if self.selected_world not in listed_levels:
                            self.selected_world = max(listed_levels)
                if event.key in {pg.K_d, pg.K_RIGHT}:
                    if self.selecting_level:
                        self.selected_level += 1
                        if self.selected_level not in listed_levels[self.selected_world]:
                            self.selected_level = min(listed_levels[self.selected_world])
                    else:
                        self.selected_world += 1
                        if self.selected_world not in listed_levels:
                            self.selected_world = min(listed_levels)

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
    raw_level: RawLevel
    pymunk_level: PymunkLevel
    surface: pg.Surface | None

    def init(self):
        self.page_name = "Game"
        super().init()
        self.surface = None

    def update(self, delta_time: float):
        super().update(delta_time)
        for event in self.get_events():
            if event.type == pg.KEYDOWN:
                pass

        self.pymunk_level.tick(delta_time)

    def draw(self, surface: pg.Surface):
        surface.fill(self.color_iter())
        if surface is not self.surface:
            self.surface = surface
            self.pymunk_level.set_pygame_screen(surface)

        self.pymunk_level.draw()

    def on_redirect_from(self, scene: BaseScene):
        super().on_redirect_from(scene)
        if not isinstance(scene, LevelSelectionScene):
            # Go back to that scene
            self.manager.set_active_scene(scene, silent=True)
            return
        self.raw_level = listed_levels[scene.selected_world][scene.selected_level]
        self.pymunk_level = PymunkLevel(self.raw_level)
