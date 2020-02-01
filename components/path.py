from dataclasses import dataclass
from typing import Deque

from .position import Position


@dataclass
class Path:
    path: Deque[Position]
