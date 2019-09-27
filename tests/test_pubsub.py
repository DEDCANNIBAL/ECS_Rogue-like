import unittest

import ecs


class TestEventQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.pubsub = ecs.PubSub()
        self.view1 = ecs.PubSubView(self.pubsub)
        self.view2 = ecs.PubSubView(self.pubsub)

    def test_append(self):
        self.view1['queue1'].append(1)
        self.assertEqual(next(self.view1['queue1']), 1)

    def test_next(self):
        self.view1['queue1'].append(1)
        self.assertEqual(next(self.view2['queue1']), 1)

    def test_next_after_clear(self):
        self.view1['queue1'].append(1)
        self.pubsub.clear()
        self.view1['queue1'].append(2)
        self.assertEqual(next(self.view2['queue1']), 2)

    def test_multiple_consumers(self):
        self.view1['queue1'].append(1)
        next(self.view1['queue1'])
        next(self.view2['queue1'])
        self.view1['queue1'].append(2)
        next(self.view1['queue1'])
        self.pubsub.clear()
        self.assertEqual(next(self.view2['queue1']), 2)
