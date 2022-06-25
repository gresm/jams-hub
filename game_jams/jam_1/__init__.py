from ..engine.window import get_game
from ..engine import scene_manager
from .scenes import MainMenu

import pygame as pg

scene_manager.spawn_scene(MainMenu)
game = get_game()


@game.frame
def frame(window: pg.Surface, delta_time: float):
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            game.stop()
        else:
            scene_manager.handle_events(ev)

    scene_manager.update()

    window.fill((0, 0, 0))

    scene_manager.draw(window)

    pg.display.update()


def main():
    game.init()
    game.run()
