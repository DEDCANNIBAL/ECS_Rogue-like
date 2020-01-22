from dataclasses import dataclass, field
from enum import Enum, auto

from components import Position


class GoalType(Enum):
    MOVE = auto()


@dataclass
class Goal:
    type: GoalType = GoalType.MOVE
    position: Position = field(default_factory=Position)
