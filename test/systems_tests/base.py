import unittest

import ecs
from ecs import PubSubView


class TestSystem(unittest.TestCase):
    system = None

    def setUp(self):
        self.registry = ecs.Registry()
        self.pubsub = ecs.PubSub()
        self.pubsub_view = PubSubView(self.pubsub)
        self.system = self.system(registry=self.registry, pubsub=self.pubsub)
