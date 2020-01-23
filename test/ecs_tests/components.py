from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Point:
    x: int = 0
    y: int = 0


@dataclass(unsafe_hash=True)
class Health:
    value: int = 10
