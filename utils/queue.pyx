#cython: language_level=3
cdef class queue:
    def __init__(self, int maxlen=1000):
        self._queue = [None for _ in range(maxlen)]
        self.l = self.r = self.size = 0
        self.maxlen = maxlen

    cpdef append(self, x):
        if self.size == self.maxlen:
            raise OverflowError
        self._queue[self.r] = x
        self.r += 1
        if self.r == self.maxlen:
            self.r = 0
        self.size += 1

    cpdef pop(self):
        if self.size == 0:
            raise IndexError('pop from empty queue')
        self._queue[self.l] = None
        self.l += 1
        if self.l == self.maxlen:
            self.l = 0
        self.size -= 1

    def __getitem__(self, int i):
        if i >= 0:
            i = self.l + i
        else:
            i = self.r + i + self.maxlen
        if i >= self.maxlen:
            i -= self.maxlen
        return self._queue[i]

    def __len__(self):
        return self.size
