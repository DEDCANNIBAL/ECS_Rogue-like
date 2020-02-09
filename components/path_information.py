from typing import Deque
from dataclasses import dataclass, field
from components import Position
from collections import deque


@dataclass
class PathInformation:
    __form_fields__ = []
    steps_from_last_update = 0
    path: Deque[Position] = field(default_factory=deque)
