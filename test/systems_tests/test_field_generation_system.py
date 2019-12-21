from components import Position, Obstacle
from systems import FieldGenerationSystem
from .base import TestSystem


class TestFieldGenerationSystem(TestSystem):
    system = FieldGenerationSystem

    def test_create_wall(self):
        self.system.create_wall(123, 5345)
        walls = [position for _, _, position in self.registry.view(Obstacle, Position)]
        self.assertListEqual([Position(123, 5345)], walls)
