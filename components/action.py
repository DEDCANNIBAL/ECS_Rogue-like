from dataclasses import dataclass, field
from enum import Enum, auto

from components import Position


class ActionType(Enum):
    MOVE = auto()


@dataclass
class Action:
    type: ActionType = ActionType.MOVE
    delta: Position = field(default_factory=Position)
    position: Position = field(default_factory=Position)
