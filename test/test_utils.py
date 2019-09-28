import unittest

from utils import queue


class TestQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = queue()

    def make_list(self):
        return [self.queue[i] for i in range(len(self.queue))]

    def test_append(self):
        self.queue.append(1)
        self.queue.append(2)
        self.assertListEqual(self.make_list(), [1, 2])

    def test_append_overflow(self):
        q = queue(0)
        self.assertRaises(OverflowError, q.append, 1)

    def test_pop(self):
        self.queue.append(1)
        self.queue.append(2)
        self.queue.pop()
        self.assertListEqual(self.make_list(), [2])

    def test_pop_empty(self):
        self.assertRaises(IndexError, self.queue.pop)

    def test_get_negative(self):
        self.queue.append(1)
        self.queue.append(2)
        self.assertEqual(self.queue[-1], 2)
