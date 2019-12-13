from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Callable

from ecs import Registry


@dataclass
class ComponentPattern:
    component: type
    args: dict


@dataclass
class ComponentPattern:
    component: type
    kwargs: dict


@dataclass
class EntityPattern:
    name: str
    component_patterns: List[ComponentPattern] = field(default_factory=list)

    def spawn(self, registry: Registry):
        pass

@lru_cache
def load(name: str):
    pass
