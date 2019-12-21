from random import randint
from math import floor

from ecs import System
from components import Obstacle, Position
from utils.getters import get_field_size


class FieldGenerationSystem(System):
    WALL_PERCENT = 0.45

    def init(self):
        field_size = get_field_size()
        self.wall_number = floor(field_size.x * field_size.y * self.WALL_PERCENT)
        walls_positions = set()
        for _ in range(self.wall_number):
            x = randint(0, field_size.x)
            y = randint(0, field_size.y)
            if (x, y) not in walls_positions:
                walls_positions.add((x, y))
                self.create_wall(x, y)

    def create_wall(self, x: int, y: int):
        self.registry.create(
            Obstacle,
            Position(x, y)
        )
