
from __future__ import annotations

import collections.abc
from functools import reduce as _reduce
import typing as t
from itertools import starmap

from .consumers import void as _void

__all__ = (
    "Star",
    "star",
    "M",
    "Mapper",
    "mapper",
)

T = t.TypeVar("T")
G = t.TypeVar("G")
P = t.ParamSpec("P")

_MISSING = object()


class Star(t.Generic[G]):
    func: t.Callable[..., G]
    def __init__(self, func: t.Callable[..., G]) -> None:
        self.func = func

    def __call__(self, args: t.Iterable[t.Any]) -> G:
        return self.func(*args)

star = Star


# TODO: Move this to Mapper Metaclass?
class MapperFactory:
    # y >= self or self <= y
    def __le__(self, iterable: t.Iterable[T]) -> Mapper[T]:
        if isinstance(iterable, collections.abc.Iterable):
            return Mapper(iterable)
        else:
            return NotImplemented

    of = __le__
    __matmul__ = __rmatmul__ = __le__

mapper = MapperFactory()


class Mapper(t.Generic[T]):
    __slots__ = ("data",)
    data: t.Iterable[T]

    def __init__(self, iterable: t.Iterable[T]) -> None:
        self.data = iterable

    def __or__(self, o: t.Callable[[T], G]) -> Mapper[G]:
        if callable(o):
            if isinstance(o, Star):
                return Mapper(starmap(o.func, self.data)) # type: ignore
            return Mapper(map(o, self.data))
        else:
            return NotImplemented

    def __gt__(self, transformer: t.Callable[[t.Iterable[T]], t.Iterable[G]]) -> Mapper[G]:
        if callable(transformer):
            return Mapper(transformer(self.data))
        else:
            return NotImplemented

    __matmul__ = __gt__
    __truediv__ = __or__

    def __ge__(self, consumer: t.Callable[[t.Iterable[T]], G]) -> G:
        if callable(consumer):
            return consumer(self.data)
        else:
            return NotImplemented

    def apply(self, transformer: t.Callable[t.Concatenate[t.Iterable[T], P], t.Iterable[G]], *args: P.args, **kwargs: P.kwargs) -> Mapper[G]:
        return Mapper(transformer(self.data, *args, **kwargs))

    def consume(self, consumer: t.Callable[t.Concatenate[t.Iterable[T], P], G], *args: P.args, **kwargs: P.kwargs) -> G:
        return consumer(self.data, *args, **kwargs)

    @t.overload
    def reduce(self, reducer: t.Callable[[T, T], T]) -> T: ...

    @t.overload
    def reduce(self, reducer: t.Callable[[G, T], G], initialiser: G) -> G: ...

    def reduce(self, reducer, initialiser = _MISSING):
        if initialiser is _MISSING:
            return _reduce(reducer, self)
        else:
            return _reduce(reducer, self, initialiser)

    def __iter__(self) -> t.Iterator[T]:
        return iter(self.data)

    def __bool__(self) -> bool:
        return bool(self.data)

    void = _void

# Alias
M = Mapper
