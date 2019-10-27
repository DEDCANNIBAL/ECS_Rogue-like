from dataclasses import dataclass
from enum import Enum, auto

from components import Position


class ActionType(Enum):
    MOVE = auto()


@dataclass
class Action:
    type: ActionType
    delta: Position = None
    position: Position = None
