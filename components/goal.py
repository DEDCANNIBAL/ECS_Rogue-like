from dataclasses import dataclass
from enum import Enum, auto

from components import Position


class GoalType(Enum):
    MOVE = auto()

@dataclass
class Goal:
    type: GoalType
    position: Position = None
