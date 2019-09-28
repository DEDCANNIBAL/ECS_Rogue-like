import unittest

import ecs


class TestSystem(unittest.TestCase):
    system = None

    def setUp(self):
        self.registry = ecs.Registry()
        self.pubsub = ecs.PubSub()
        self.system = self.system(registry=self.registry, pubsub=self.pubsub)
