#cython: language_level=3
# distutils: language = c++

cdef class PubSub:
    cdef:
        dict queues
    cpdef clear(self)

cdef class PubSubView:
    cdef:
        PubSub pubsub
        dict queues_views
