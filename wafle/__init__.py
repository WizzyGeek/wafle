
from __future__ import annotations

import collections.abc
from functools import reduce as _reduce
import typing as t
from itertools import starmap, zip_longest


__all__ = (
    "Star",
    "star",
    "M",
    "Mapper",
    "mrange",
    "rpartial",
    "mzip",
    "mzip_longest",
    "with_predicate",
    "with_rightargs",
    "mapper",
)

T = t.TypeVar("T")
G = t.TypeVar("G")
P = t.ParamSpec("P")

_MISSING = object()

class Star(t.Generic[G]):
    def __init__(self, func: t.Callable[..., G]) -> None:
        self.func = func

    def __call__(self, args: t.Iterable[t.Any]) -> G:
        return self.func(*args)

star = Star

class MapperFactory:
    # y >= self or self <= y
    def __le__(self, iterable: t.Iterable[T]) -> Mapper[T]:
        if isinstance(iterable, collections.abc.Iterable):
            return Mapper(iterable)
        else:
            return NotImplemented

    of = __le__

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


# Alias
M = Mapper


if t.TYPE_CHECKING:
    _T3 = t.TypeVar("_T3")
    _T4 = t.TypeVar("_T4")

@t.overload
def mzip(*, strict: bool = False) -> Mapper[t.Any]: ...

@t.overload
def mzip(iter1: t.Iterable[T], /, *, strict: bool = False) -> Mapper[tuple[T]]: ...

@t.overload
def mzip(iter1: t.Iterable[T], iter2: t.Iterable[G], /, *, strict: bool = False) -> Mapper[tuple[T, G]]: ...

@t.overload
def mzip(iter1: t.Iterable[T], iter2: t.Iterable[G], iter3: t.Iterable[_T3], /, *, strict: bool = False) -> Mapper[tuple[T, G, _T3]]: ...


def mzip(*iterables: t.Iterable[t.Any], strict: bool = False) -> Mapper[tuple[t.Any, ...]]:
    return Mapper(zip(*iterables, strict=strict))


@t.overload
def mzip_longest(*, fillvalue: t.Any = None) -> Mapper[t.Any]: ...

@t.overload
def mzip_longest(iter1: t.Iterable[T], /, *, fillvalue: _T4) -> Mapper[tuple[T | _T4]]: ...

@t.overload
def mzip_longest(iter1: t.Iterable[T], iter2: t.Iterable[G], /, *, fillvalue: _T4) -> Mapper[tuple[T | _T4, G | _T4]]: ...

@t.overload
def mzip_longest(iter1: t.Iterable[T], iter2: t.Iterable[G], iter3: t.Iterable[_T3], /, *, fillvalue: _T4) -> Mapper[tuple[T | _T4, G | _T4, _T3 | _T4]]: ...

@t.overload
def mzip_longest(iter1: t.Iterable[T], /) -> Mapper[tuple[T | None]]: ...

@t.overload
def mzip_longest(iter1: t.Iterable[T], iter2: t.Iterable[G], /) -> Mapper[tuple[T | None, G | None]]: ...

@t.overload
def mzip_longest(iter1: t.Iterable[T], iter2: t.Iterable[G], iter3: t.Iterable[_T3], /) -> Mapper[tuple[T | None, G | None, _T3 | None]]: ...


def mzip_longest(*iterables: t.Iterable[t.Any], fillvalue: t.Any = None) -> Mapper[tuple[t.Any, ...]]:
    return Mapper(zip_longest(*iterables, fillvalue=fillvalue))


# t.reveal_type(mzip(range(1), range(2)))
# t.reveal_type(mzip(range(1), range(1), range(1), range(1), range(1), range(1), range(1),))

@t.overload
def mrange(stop: int, /) -> Mapper[int]: ...

@t.overload
def mrange(start: int, stop: int, /) -> Mapper[int]: ...

@t.overload
def mrange(start: int, stop: int, step: int, /) -> Mapper[int]: ...

def mrange(*args: int) -> Mapper[int]:
    return Mapper(range(*args))

def rpartial(func, /, *args, **keywords):
    """creates a partial where the supplied positional arguments
    are supplied as the right most positional arguments in order
    """
    def newfunc(*fargs, **fkeywords):
        newkeywords = {**keywords, **fkeywords}
        return func(*fargs, *args, **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

def with_predicate(func: t.Callable[[T, G], _T3]) -> t.Callable[[T], t.Callable[[G], _T3]]:
    def get_predicate(predicate: T) -> t.Callable[[G], _T3]:
        def call(iterable: G) -> _T3:
            return func(predicate, iterable)
        return call
    return get_predicate

def with_rightargs(func: t.Callable[t.Concatenate[T, P], G]) -> t.Callable[P, t.Callable[[T], G]]:
    def get_rightargs(*args: P.args, **kwargs: P.kwargs) -> t.Callable[[T], G]:
        def call(iterable: T) -> G:
            return func(iterable, *args, **kwargs)
        return call
    return get_rightargs
