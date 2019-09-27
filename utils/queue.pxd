#cython: language_level=3
cdef class queue:
    cdef:
        public list _queue
        public int l, r, size, maxlen
    cpdef append(self, x)
    cpdef pop(self)
