from ..engine import BaseScene
from . import assets

import pygame as pg


class MainMenu(BaseScene):
    def init(self):
        pg.display.set_caption("Top and Bottom - Main Menu")

    def draw(self, surface: pg.Surface):
        surface.blit(assets.font_title.render("Main Menu", True, (255, 255, 255)), (10, 10))
        surface.blit(assets.font_text.render("Press Enter to start", True, (255, 255, 255)), (10, 30))
        surface.blit(assets.font_text.render("Press Escape to quit", True, (255, 255, 255)), (10, 50))
