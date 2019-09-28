import sys
import unittest

import ecs


class TestEventQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = ecs.EventQueue()
        self.view1 = ecs.EventQueueView(self.queue)
        self.view2 = ecs.EventQueueView(self.queue)

    def test_append(self):
        self.view1.append(1)
        self.assertEqual(next(self.view1), 1)

    def test_iter(self):
        self.view1.append(1)
        self.view2.append(2)
        self.view1.append(3)
        self.assertListEqual(list(self.view1), [1, 2, 3])
        self.view2.append(4)
        self.assertListEqual(list(self.view2), [1, 2, 3, 4])
        self.assertListEqual(list(self.view1), [4])

    def test_append_after_clear(self):
        self.view1.append(1)
        next(self.view1)
        next(self.view2)
        self.queue.clear()
        self.view1.append(2)
        self.assertEqual(next(self.view1), 2)

    def test_clear_unseen(self):
        self.view1.append(1)
        self.view2.subscribe()
        next(self.view1)
        self.queue.clear()
        self.assertEqual(len(self.queue), 1)

    def test_clear_seen(self):
        obj = []
        self.view1.append(obj)
        next(self.view1)
        next(self.view2)
        self.queue.clear()
        self.assertEqual(len(self.queue), 0)
        self.assertEqual(sys.getrefcount(obj), 2)

    def test_next(self):
        self.view1.append((1, 2))
        self.assertEqual(next(self.view1), (1, 2))
        self.assertEqual(next(self.view2), (1, 2))

    def test_next_from_empty(self):
        self.assertRaises(StopIteration, next, self.view1)


class TestSmallEventQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = ecs.EventQueue(maxlen=3)
        self.view1 = ecs.EventQueueView(self.queue)
        self.view2 = ecs.EventQueueView(self.queue)

    def test_append(self):
        self.view1.append(1)
        self.view1.append(2)
        self.view1.append(3)
        self.assertEqual(next(self.view1), 1)

    def test_iter(self):
        self.view1.append(1)
        self.view2.append(2)
        self.assertListEqual(list(self.view1), [1, 2])
        self.view2.append(3)
        self.assertListEqual(list(self.view2), [1, 2, 3])
        self.assertListEqual(list(self.view1), [3])

    def test_append_after_clear(self):
        self.view1.append(1)
        self.view1.append(2)
        self.view1.append(3)
        next(self.view1)
        next(self.view2)
        self.queue.clear()
        self.view1.append(4)
        self.assertListEqual(list(self.view2), [2, 3, 4])

    def test_overflow(self):
        self.view1.append(1)
        self.view1.append(2)
        self.view1.append(3)
        self.assertRaises(OverflowError, self.queue.append, 1)

    def test_full_clear(self):
        self.view1.append(1)
        self.view1.append(2)
        self.view1.append(3)
        list(self.view1), list(self.view2)
        self.queue.clear()
        self.view2.append(4)
        self.assertEqual(next(self.view1), 4)

    def test_new_view(self):
        self.view1.append(1)
        view = ecs.EventQueueView(self.queue)
        self.assertEqual(next(view), 1)

    def test_new_view_after_clear(self):
        self.view1.append(1)
        next(self.view1), next(self.view2)
        self.queue.clear()
        self.view2.append(2)
        view = ecs.EventQueueView(self.queue)
        self.assertEqual(next(view), 2)

    def test_append_tricky(self):
        self.view1.append(1)
        next(self.view1)
        self.queue.clear()
        self.view1.append(2)
        self.view1.append(3)
        self.view1.append(4)
        self.assertEqual(next(self.view1), 2)
