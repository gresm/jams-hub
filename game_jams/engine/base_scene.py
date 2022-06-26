from __future__ import annotations

from typing import Type

import pygame as pg

from .window import GameState
from .scene_tools import FrameCounter


class SceneException(Exception):
    pass


class Scene:
    _instances_cnt: int = -1
    instances: dict[int, Scene] = {}

    _scenes_cnt = -1
    scenes: dict[int, Type[Scene]] = {}

    class_id: int = -1

    manager: SceneManager | None
    frame_counter: FrameCounter

    def __init__(self, scene_manager: SceneManager):
        self.manager = scene_manager
        Scene._instances_cnt += 1
        Scene.instances[self._instances_cnt] = self
        self.instance_id = self.current_instance_id()
        self._events: list[pg.event.Event] = []
        self.frame_counter = FrameCounter(self.manager.game.max_fps)
        self.init()

    def __init_subclass__(cls, **kwargs):
        Scene._scenes_cnt += 1
        Scene.scenes[Scene._scenes_cnt] = cls
        cls.class_id = cls.current_class_id()

    @classmethod
    def current_instance_id(cls):
        return Scene._instances_cnt

    @classmethod
    def current_class_id(cls):
        return Scene._scenes_cnt

    def init(self, *args, **kwargs):
        pass

    def add_event_to_pool(self, event: pg.event.Event):
        self._events.append(event)

    def on_event(self, event: pg.event.Event):
        pass

    def get_events(self):
        for _ in range(len(self._events)):
            yield self._events.pop()

    def draw(self, surface: pg.Surface):
        pass

    def update(self):
        pass

    def on_redirect(self, scene: Scene):
        pass

    def on_redirect_from(self, scene: Scene):
        pass


class SceneManager:
    game: GameState
    global_counter: FrameCounter

    def __init__(self):
        self.current: Scene | None = None
        self.initialised = False

    def init_check(self):
        if not self.initialised:
            raise SceneException("SceneManager not initialised")

    def draw(self, surface: pg.Surface):
        self.init_check()
        if self.current is not None:
            self.current.draw(surface)

    def update(self):
        self.init_check()
        if self.current:
            self.current.update()
            self.current.frame_counter.tick()

    def set_active_scene(self, scene_id: int | Scene):
        if isinstance(scene_id, Scene):
            if self.current:
                self.current.on_redirect(scene_id)
            old = self.current
            self.current = scene_id
            self.current.on_redirect_from(old)
        elif scene_id in Scene.instances:
            old = self.current
            new = Scene.instances[scene_id]
            new.on_redirect_from(old)
            if self.current:
                self.current.on_redirect(new)
            self.current = new

    def spawn_scene(self, scene_id: int | Type[Scene]):
        if isinstance(scene_id, type) and issubclass(scene_id, Scene):
            return self.spawn_scene(scene_id.class_id)
        elif scene_id in Scene.scenes:
            Scene.scenes[scene_id](self)
            self.set_active_scene(Scene.current_instance_id())
            return Scene.current_instance_id()
        else:
            raise SceneException("Scene not found.")

    def spawn_remove_scene(self, scene_id: int | Type[Scene]):
        self.remove_scene(Scene.current_instance_id())
        self.spawn_scene(scene_id)

    def remove_scene(self, scene_id: int | Scene):
        if isinstance(scene_id, Scene):
            scene_id = scene_id.instance_id
        if scene_id in Scene.instances:
            del Scene.instances[scene_id]
            if self.current and scene_id == self.current.instance_id:
                self.current = None

    def handle_events(self, event: pg.event.Event):
        self.current.add_event_to_pool(event)
        self.current.on_event(event)

    def init(self, game: GameState, *args, **kwargs):
        self.game = game
        self.global_counter = FrameCounter(self.game.max_fps)
        self.initialised = True

        if self.current:
            self.current.init(*args, **kwargs)
