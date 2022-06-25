from ..engine import BaseScene
from . import assets

import pygame as pg


class MainMenu(BaseScene):
    frame_counter: int = 0

    def init(self):
        pg.display.set_caption("Top and Bottom - Main Menu")

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

    def draw(self, surface: pg.Surface):
        surface.blit(assets.font_title.render("Main Menu", True, (255, 255, 255)), (10, 10))
        surface.blit(assets.font_text.render("Press Enter to start", True, (255, 255, 255)), (10, 50))
        surface.blit(assets.font_text.render("Press Escape to quit", True, (255, 255, 255)), (10, 80))


class GameScene(BaseScene):
    pass
