# distutils: language = c++
#cython: language_level=3
import cython
from libc.math cimport sqrt

@cython.freelist(32)
cdef class vec2i:
    cdef public int x, y
