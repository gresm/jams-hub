from ..engine import BaseScene
from . import assets, color_permutations

import pygame as pg


class MainMenu(BaseScene):
    frame_counter: int = 0
    current_color: tuple[int, int, int, bool]

    def init(self):
        pg.display.set_caption("Top and Bottom - Main Menu")
        self.current_color = (0, 0, 0, True)

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
        self.current_color = color_permutations.simple_color_iter(*self.current_color)

    def draw(self, surface: pg.Surface):
        surface.fill(self.current_color[:3])
        surface.blit(assets.font_title.render("Main Menu", True, (255, 255, 255)), (10, 10))
        surface.blit(assets.font_text.render("Press Enter to start", True, (255, 255, 255)), (10, 50))
        surface.blit(assets.font_text.render("Press Escape to quit", True, (255, 255, 255)), (10, 80))


class GameScene(BaseScene):
    pass
