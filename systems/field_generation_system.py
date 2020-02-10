from random import randint
from math import floor

from ecs import System
from components import Obstacle, Position
from settings import WALL_PERCENT
from getters import get_field_size
import patterns


class FieldGenerationSystem(System):
    def init(self):
        field_size = get_field_size()
        self.wall_number = floor(field_size.x * field_size.y * WALL_PERCENT)
        self.create_bounds()
        obstacles = {pos for *_, pos in self.registry.view(Obstacle, Position)}
        for _ in range(self.wall_number):
            x = randint(1, field_size.x - 1)
            y = randint(1, field_size.y - 1)
            if Position(x, y) not in obstacles:
                obstacles.add((x, y))
                self.create_wall(x, y)

    def create_wall(self, x: int, y: int):
        patterns.load('wall').spawn(self.registry, Position(x, y))

    def create_bounds(self):
        field_size = get_field_size()
        for i in range(field_size.x):
            self.create_wall(i, 0)
            self.create_wall(i, field_size.y - 1)
        for i in range(field_size.y):
            self.create_wall(0, i)
            self.create_wall(field_size.x - 1, i)
