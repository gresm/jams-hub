"""
Convert RawLevel to pymunk space for physics simulation.
"""
from __future__ import annotations

from raw_level import RawLevel, Tile
from enum import Enum
import pymunk


class CollisionMasks(Enum):
    players = 1
    walls = 4
    goals = 8
    movable = 16
    level_boundary = 32
    movable_go_through_boundary = 64
    player_collide_with = 125  # walls | movable | goals | level_boundary | movable_go_through_boundary | players
    movable_collide_with = 53  # walls | movable | players | level_boundary


class PymunkLevel:
    def __init__(self, level: RawLevel):
        self.raw_level = level
        self.space = pymunk.Space()
        self.players: set[pymunk.Shape] = set()
        self.goals: set[pymunk.Shape] = set()
        self.player_goal_collision_handler = self.space.add_collision_handler(
            CollisionMasks.players.value, CollisionMasks.goals.value
        )

        self.activated_goals: int = 0

        self.player_goal_collision_handler.pre_solve = self.player_goal_pre_solve
        self.player_goal_collision_handler.separate = self.player_goal_separate

    def player_goal_pre_solve(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data) -> bool:
        self.activated_goals += 1
        return False

    def player_goal_separate(self, arbiter, space, data):
        self.activated_goals -= 1

    def add_wall(self, row_index, col_index):
        """
        Add wall to space.
        """
        wall_shape = pymunk.Poly(self.space.static_body,
                                 [(col_index * 32, row_index * 32), (col_index * 32 + 32, row_index * 32),
                                  (col_index * 32 + 32, row_index * 32 + 32),
                                  (col_index * 32, row_index * 32 + 32)])
        wall_shape.friction = 0.5
        wall_shape.collision_type = CollisionMasks.walls.value
        wall_shape.filter = pymunk.ShapeFilter(CollisionMasks.player_collide_with.value,
                                               CollisionMasks.movable_collide_with.value)
        self.space.add(wall_shape)

    def add_goal(self, row_index, col_index):
        """
        Add goal to space.
        """
        goal_shape = pymunk.Circle(self.space.static_body, 16, (col_index * 32 + 16, row_index * 32 + 16))
        goal_shape.friction = 0.5
        goal_shape.collision_type = CollisionMasks.goals.value
        goal_shape.filter = pymunk.ShapeFilter(CollisionMasks.player_collide_with.value,
                                               CollisionMasks.movable_collide_with.value)
        self.space.add(goal_shape)
        self.goals.add(goal_shape)

    def add_movable(self, row_index, col_index):
        """
        Add movable to space.
        """
        movable_shape = pymunk.Poly(self.space.static_body,
                                    [(col_index * 28, row_index * 28), (col_index * 28 + 28, row_index * 28),
                                     (col_index * 28 + 28, row_index * 28 + 28),
                                     (col_index * 28, row_index * 28 + 28)])
        movable_shape.friction = 0.5
        movable_shape.collision_type = CollisionMasks.movable.value
        movable_shape.filter = pymunk.ShapeFilter(CollisionMasks.player_collide_with.value,
                                                  CollisionMasks.movable_collide_with.value)
        self.space.add(movable_shape)

    def add_player(self, row_index, col_index):
        """
        Add player to space.
        """
        player_shape = pymunk.Circle(self.space.static_body, 16, (col_index * 32 + 16, row_index * 32 + 16))
        player_shape.friction = 0.5
        player_shape.collision_type = CollisionMasks.players.value
        player_shape.filter = pymunk.ShapeFilter(CollisionMasks.player_collide_with.value,
                                                 CollisionMasks.movable_collide_with.value)
        self.space.add(player_shape)
        self.players.add(player_shape)

    def populate_space(self):
        """
        Fill space with bodies and shapes from raw level.
        """
        for row_index, row in enumerate(self.raw_level.upper_board):
            for col_index, tile in enumerate(row):
                if tile == Tile.wall:
                    self.add_wall(row_index, col_index)
                elif tile == Tile.player:
                    self.add_player(row_index, col_index)
                elif tile == Tile.goal:
                    self.add_goal(row_index, col_index)
                elif tile == Tile.movable:
                    self.add_movable(row_index, col_index)
