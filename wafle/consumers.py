
from __future__ import annotations

from collections import deque as _deque
import typing as t

__all__ = (
    "void",
)


# Fastest method to consume an iterable
# TODO: Search for faster methods
def void(iterator: t.Iterable) -> None:
    _deque(iterator, maxlen=0)
    return None