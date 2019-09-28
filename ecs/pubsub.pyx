#cython: language_level=3
from ecs.event_queue cimport EventQueue, EventQueueView


cdef class PubSub:
    def __init__(self):
        self.queues = {}

    def  __getitem__(self, str item):
        cdef EventQueue queue = self.queues.get(item)
        if queue is None:
            queue = EventQueue()
            self.queues[item] = queue
        return queue

    def __getattr__(self, str item):
        return self[item]

    cpdef clear(self):
        for queue in self.queues.values():
            queue.clear()


cdef class PubSubView:
    def __init__(self, PubSub pubsub):
        self.pubsub = pubsub
        self.queues_views = {}

    def  __getitem__(self, str item):
        cdef EventQueueView queue_view = self.queues_views.get(item)
        if queue_view is None:
            queue_view = EventQueueView(self.pubsub[item])
            self.queues_views[item] = queue_view
        return queue_view

    def __getattr__(self, str item):
        return self[item]
