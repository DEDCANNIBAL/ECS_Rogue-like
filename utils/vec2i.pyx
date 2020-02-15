# distutils: language = c++
#cython: language_level=3
import cython

cdef class vec2i:
    def __init__(self, int x=0, int y=0):
        self.x = x
        self.y = y

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(vec2i self, vec2i other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(vec2i self, vec2i other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(vec2i self, int other):
        return type(self)(self.x * other, self.y * other)

    def __floordiv__(vec2i self, int other):
        return type(self)(self.x // other, self.y // other)

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

    def __hash__(self):
        return self.x << 16 ^ self.y

    def __ne__(self, other):
        return not self == other

    def __lt__(vec2i self, vec2i other):
        return self.x < other.x \
               and self.y < other.y

    def __le__(vec2i self, vec2i other):
        return self.x <= other.x \
               and self.y <= other.y

    def __gt__(vec2i self, vec2i other):
        return self.x > other.x \
               and self.y > other.y

    def __ge__(vec2i self, vec2i other):
        return self.x >= other.x \
               and self.y >= other.y
