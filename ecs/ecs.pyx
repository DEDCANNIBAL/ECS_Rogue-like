from functools import lru_cache
from typing import Any

import cython


cdef class defaultdict(dict):
    def __getitem__(self, type i):
        t = super().get(i)
        if t is None:
            t = dict()
            super().__setitem__(i, t)
        return t


ctypedef fused type_or_component:
    type
    object

cdef class Registry:
    cdef :
        int counter
        public defaultdict components

    def __cinit__(self):
        self.counter = 0
        self.components = defaultdict()

    def create(self, *components) -> int:
        cdef int entity = self.counter
        self.counter += 1
        for component in components:
            self.assign(entity, component)
        return entity

    cpdef assign(self, int entity, component):
        if isinstance(component, type):
            self.components[component][entity] = component()
        else:
            self.components[type(component)][entity] = component

    def get(self, int entity, *components):
        return [self.components[component].get(entity) for component in components]

    def view(self, *other_components):
        if len(other_components) == 1:
            yield from self.components[other_components[0]].items()
            return
        min_component = min(other_components, key=lambda component_type: len(self.components[component_type]))
        other_components = [component for component in other_components if component is not min_component]
        for entity, first_component_instance in self.components[min_component].items():
            result = self.get_other_components(other_components, entity, first_component_instance)
            if result is not None: yield result

    cdef list get_other_components(self, list other_components, int entity, first_component_instance):
        cdef list result = [entity, first_component_instance]
        for component in other_components:
            other_component_instance = self.components[component].get(entity)
            if other_component_instance is None:
                return None
            else:
                result.append(other_component_instance)
        else:
            return result

    cdef int count_components(self, type component_type):
        return len(self.components[component_type])


cdef class System:
    cdef Registry registry

    def __cinit__(self, Registry registry):
        self.registry = registry

    def process(self, dt):
        raise NotImplementedError

    def init(self):
        raise NotImplementedError


