#cython: language_level=3

cdef class EventQueue:
    def __init__(self, int maxlen=1000):
        maxlen += 1
        self.events = [None for _ in range(maxlen)]
        self.pointers.resize(maxlen)
        self.subscribers_number = 0
        self.maxlen = maxlen
        self.l = self.r = self.size = 0

    cpdef append(self, x):
        if self.size == self.maxlen - 1:
            raise OverflowError
        self.events[self.r] = x
        self.pointers[self.r] = 0
        self.r += 1
        if self.r == self.maxlen:
            self.r = 0
        self.size += 1

    cpdef clear(self):
        while self.size and self.pointers[self.l] >= self.subscribers_number:
            self.pop()

    cpdef pop(self):
        if self.size == 0:
            raise IndexError('pop from empty queue')
        self.events[self.l] = None
        self.l += 1
        if self.l == self.maxlen:
            self.l = 0
        self.size -= 1

    def __len__(self):
        return self.size


cdef class EventQueueView:
    def __init__(self, EventQueue event_queue):
        self.event_queue = event_queue
        self.is_subscribed = False

    cpdef append(self, x):
        self.event_queue.append(x)

    def __del__(self):
        self.unsubscribe()

    def __iter__(self):
        return self

    def __next__(self):
        self.subscribe()
        if self.i == self.event_queue.r:
            raise StopIteration
        self.event_queue.pointers[self.i] += 1
        cdef object ans = self.event_queue.events[self.i]

        self.i += 1
        if self.i == self.event_queue.maxlen:
            self.i = 0

        return ans

    cpdef subscribe(self):
        if not self.is_subscribed:
            self.i = self.event_queue.l
            self.event_queue.subscribers_number += 1
            self.is_subscribed = True

    cpdef unsubscribe(self):
        if self.is_subscribed:
            self.event_queue.subscribers_number -= 1
            self.is_subscribed = False

    def __len__(self):
        return self.event_queue.size
