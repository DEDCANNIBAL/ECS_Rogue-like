from typing import Deque
from dataclasses import dataclass
from components import Position


@dataclass
class Path:
    path: Deque[Position]
