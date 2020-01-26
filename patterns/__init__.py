import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import List

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import components  # For yaml
from ecs import Registry

PATH_TO_PATTERNS = Path('patterns') / 'patterns'


@dataclass
class ComponentPattern:
    component: type
    kwargs: dict = field(default_factory=dict)


@dataclass
class EntityPattern:
    name: str
    component_patterns: List[ComponentPattern] = field(default_factory=list)

    def spawn(self, registry: Registry):
        components = [
            component_pattern.component(**component_pattern.kwargs)
            for component_pattern in self.component_patterns
        ]
        return registry.create(*components), *components

    def save(self):
        serialized_pattern = yaml.dump(self, Dumper=Dumper)
        with (PATH_TO_PATTERNS / self.name).open('w') as file:
            file.write(serialized_pattern)

    def delete(self):
        os.remove(PATH_TO_PATTERNS / self.name)


@lru_cache
def load(name: str) -> EntityPattern:
    with (PATH_TO_PATTERNS / name).open() as file:
        serialized = file.read()
        return yaml.load(serialized, Loader=Loader)
