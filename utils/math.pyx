#cython: language_level=3


def sign(int x):
    return 1 if x > 0 else (-1 if x < 0 else 0)
