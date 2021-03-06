import unittest

import ecs
from patterns import EntityPattern, ComponentPattern, load
from test.ecs_tests.components import Health, Point


class TestPatterns(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = ecs.Registry()
        self.name = 'test'

    def test_save_load(self):
        entity_pattern = EntityPattern(self.name, component_patterns=[
            ComponentPattern(Health, {'value': 4}),
            ComponentPattern(Point, {'x': 2, 'y': 3}),
        ])
        entity_pattern.save()
        entity_pattern_loaded = load(self.name)
        self.assertEqual(entity_pattern, entity_pattern_loaded)
        entity_pattern_loaded.delete()

    def test_spawn(self):
        entity_pattern = EntityPattern(self.name, component_patterns=[
            ComponentPattern(Point, {'x': 2}),
            ComponentPattern(Health, {'value': 4}),
        ])
        entity = entity_pattern.spawn(self.registry)
        self.assertListEqual(
            list(self.registry.get(entity, Point, Health)),
            [Point(2, 0), Health(4)]
        )

    def test_spawn_replace_components(self):
        entity_pattern = EntityPattern(self.name, component_patterns=[
            ComponentPattern(Point, {'x': 2}),
            ComponentPattern(Health, {'value': 4}),
        ])
        entity = entity_pattern.spawn(self.registry, Health(5))
        self.assertListEqual(
            list(self.registry.get(entity, Point, Health)),
            [Point(2, 0), Health(5)]
        )
