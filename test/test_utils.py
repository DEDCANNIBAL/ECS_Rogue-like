import unittest

from utils import queue, itertools
from utils.vec2i import vec2i


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


class TestVec2i(unittest.TestCase):
    def test_abs(self):
        self.assertEqual(abs(vec2i(1, -1)), 2 ** 0.5)

    def test_add(self):
        self.assertEqual(vec2i(1, -1) + vec2i(2, 1), vec2i(3, 0))

    def test_sub(self):
        self.assertEqual(vec2i(2, 1) - vec2i(1, 2), vec2i(1, -1))

    def test_iadd(self):
        v = vec2i(2, 1)
        v += vec2i(0, 1)
        self.assertEqual(v, vec2i(2, 2))

    def test_isub(self):
        v = vec2i(2, 1)
        v -= vec2i(0, 1)
        self.assertEqual(v, vec2i(2, 0))

    def test_mul(self):
        self.assertEqual(vec2i(2, -1) * 2, vec2i(4, -2))

    def test_div(self):
        self.assertEqual(vec2i(4, -2) // 2, vec2i(2, -1))


class TestItertools(unittest.TestCase):
    def test_last(self):
        self.assertEqual(itertools.last(range(3)), 2)

    def test_empty(self):
        self.assertIs(itertools.last([]), None)
