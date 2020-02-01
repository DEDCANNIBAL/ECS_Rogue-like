import unittest
from typing import Optional

import ecs
from ecs import PubSubView, System


class TestSystem(unittest.TestCase):
    system: Optional[System] = None

    def setUp(self):
        self.registry = ecs.Registry()
        self.pubsub = ecs.PubSub()
        self.pubsub_view = PubSubView(self.pubsub)
        self.system = self.system(registry=self.registry, pubsub=self.pubsub)
