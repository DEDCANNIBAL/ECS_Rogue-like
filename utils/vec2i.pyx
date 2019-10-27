#cython: language_level=3
import cython
from libc.math cimport sqrt


@cython.freelist(32)
cdef class vec2i:
    cdef public int x, y

    def __init__(self, int x, int y):
        self.x = x
        self.y = y

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(vec2i self, vec2i other):
        return vec2i(self.x + other.x, self.y + other.y)

    def __sub__(vec2i self, vec2i other):
        return vec2i(self.x - other.x, self.y - other.y)

    def __mul__(vec2i self, int other):
        return vec2i(self.x * other, self.y * other)

    def __floordiv__(vec2i self, int other):
        return vec2i(self.x // other, self.y // other)

    def __eq__(vec2i self, vec2i other):
        return self.x == other.x and self.y == other.y

    def __iadd__(vec2i self, vec2i other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(vec2i self, vec2i other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __str__(self):
        return f'{self.x}, {self.y}'
