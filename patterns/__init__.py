import inspect
from copy import copy
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List

from ecs import Registry


class ComponentPattern:
    def __init__(self, component: type):
        self.component = component
        self.kwargs = {key: value for key, value in inspect.getmembers(component()) if not key.startswith('__')}


@dataclass
class EntityPattern:
    name: str
    component_patterns: List[ComponentPattern] = field(default_factory=list)

    def spawn(self, registry: Registry):
        pass


@lru_cache
def load(name: str):
    pass
