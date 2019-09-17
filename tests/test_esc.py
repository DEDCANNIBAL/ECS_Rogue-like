import unittest

import ecs
from tests.components import Health, Point


class TestEscpp(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = ecs.Registry()

    def test_create_empty(self):
        entity1 = self.registry.create()
        entity2 = self.registry.create()
        self.assertNotEqual(entity1, entity2)

    def test_create_default(self):
        entity = self.registry.create(Health)
        self.assertIsInstance(self.registry.get(entity, Health)[0], Health)

    def test_create(self):
        point = Point(3, 4)
        entity = self.registry.create(point)
        self.assertIs(self.registry.get(entity, Point)[0], point)

    def test_assign_default(self):
        entity = self.registry.create()
        self.registry.assign(entity, Health)
        self.assertIsInstance(self.registry.get(entity, Health)[0], Health)

    def test_assign(self):
        entity = self.registry.create()
        point = Point(3, 4)
        self.registry.assign(entity, point)
        self.assertIs(self.registry.get(entity, Point)[0], point)

    def test_view_one(self):
        hp1, hp2, point = Health(), Health(), Point()
        entity1 = self.registry.create(hp1)
        entity2 = self.registry.create(hp2, point)
        self.assertEqual(
            {tuple(row) for row in self.registry.view(Health)},
            {(entity1, hp1), (entity2, hp2)}
        )
        self.assertEqual(
            {tuple(row) for row in self.registry.view(Point)},
            {(entity2, point)}
        )

    def test_view_two(self):
        hp, point = Health(), Point()
        entity = self.registry.create(hp, point)
        self.assertEqual(
            {tuple(row) for row in self.registry.view(Health, Point)},
            {(entity, hp, point)}
        )
