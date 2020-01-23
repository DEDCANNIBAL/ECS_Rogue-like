import sys
import unittest

import ecs
from .components import Health, Point


class TestRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = ecs.Registry()

    def test_create_empty(self):
        entity1 = self.registry.create()
        entity2 = self.registry.create()
        self.assertNotEqual(entity1, entity2)

    def test_create_default(self):
        entity = self.registry.create(Health)
        self.assertIsInstance(self.registry.get(entity, Health), Health)

    def test_create(self):
        point = Point(3, 4)
        entity = self.registry.create(point)
        self.assertIs(self.registry.get(entity, Point), point)

    def test_assign_default(self):
        entity = self.registry.create()
        self.registry.assign(entity, Health)
        self.assertIsInstance(self.registry.get(entity, Health), Health)

    def test_assign_with_args(self):
        entity = self.registry.create()
        self.registry.assign(entity, Point, 3, 4)
        self.assertEqual(self.registry.get(entity, Point), Point(3, 4))

    def test_assign_with_kwargs(self):
        entity = self.registry.create()
        self.registry.assign(entity, Point, x=3, y=4)
        self.assertEqual(self.registry.get(entity, Point), Point(3, 4))

    def test_assign(self):
        entity = self.registry.create()
        point = Point(3, 4)
        self.registry.assign(entity, point)
        self.assertIs(self.registry.get(entity, Point), point)

    def test_get_few(self):
        hp, point = Health(), Point()
        entity = self.registry.create(point, hp)
        self.assertEqual(
            tuple(self.registry.get(entity, Point, Health)),
            (point, hp)
        )

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

    def test_view_optimization(self):
        self.registry.create(Health, Point)
        self.registry.create(Health)
        entity, hp, point = next(self.registry.view(Health, Point))
        self.assertIsInstance(hp, Health)
        self.assertIsInstance(point, Point)

    def test_delete(self):
        hp = Health()
        entity = self.registry.create(hp)
        self.registry.delete(entity)
        self.assertIsNone(self.registry.get(entity, Health))
        self.assertEqual(sys.getrefcount(hp), 2)

    def test_remove(self):
        entity = self.registry.create(Health)
        self.registry.remove(entity, Health)
        self.assertIsNone(self.registry.get(entity, Health))


class TestSystemManager(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = ecs.Registry()
        self.pubsub = ecs.PubSub()
        self.manager = ecs.SystemManager(pubsub=self.pubsub, registry=self.registry)
        self.system = TestSystem()

    def test_init_default(self):
        manager = ecs.SystemManager()
        self.assertIsInstance(manager.registry, ecs.Registry)
        self.assertIsInstance(manager.pubsub, ecs.PubSub)

    def test_add_system_instance(self):
        self.manager.add_system(self.system)
        self.assertIs(self.system.registry, self.registry)
        self.assertIsInstance(self.system.pubsub, ecs.PubSubView)
        self.assertTrue(self.system.initialized)

    def test_add_system(self):
        self.manager.add_system(TestSystem)

    def test_process(self):
        self.manager.add_system(self.system)
        self.manager.process(1)
        self.assertTrue(self.system.processed)


class TestSystem(ecs.System):
    def __init__(self, *args):
        super().__init__(*args)
        self.initialized = False
        self.processed = False

    def process(self, dt):
        self.processed = True

    def init(self):
        self.initialized = True
