#cython: language_level=3
# distutils: language = c++

from libcpp.vector cimport vector

cdef class EventQueue:
    cdef:
        list events
        vector[int] pointers
        int subscribers_number, maxlen, l, r, size
    cpdef append(self, x)
    cpdef pop(self)
    cpdef clear(self)

cdef class EventQueueView:
    cdef:
        EventQueue event_queue
        int i
        char is_subscribed
    cpdef append(self, x)
    cpdef subscribe(self)
    cpdef unsubscribe(self)
