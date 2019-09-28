from dataclasses import dataclass


@dataclass
class Actable:
    is_player: bool = False
    acted: bool = False
