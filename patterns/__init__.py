from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Callable

from ecs import Registry


@dataclass
class ComponentPattern:
    component: type
    args: dict


@dataclass
class Pattern:
    name: str
    component_factories: List[Callable] = field(default_factory=list)

    def spawn(self, registry: Registry):
        return registry.create(*[Factory() for Factory in self.component_factories])


@lru_cache
def load(name: str):
    pass
