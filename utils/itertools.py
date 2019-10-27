from typing import Iterable, TypeVar, Optional

T = TypeVar('T')


def last(d: Iterable[T]) -> Optional[T]:
    x = None
    for x in d:
        pass
    return x
