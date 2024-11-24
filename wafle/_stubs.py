from __future__ import annotations

from functools import partial as _p
import typing as t
from itertools import zip_longest

from .mapper import Mapper


if t.TYPE_CHECKING:
    T = t.TypeVar("T")
    G = t.TypeVar("G")
    P = t.ParamSpec("P")
    Ts = t.TypeVarTuple("Ts")
    T3 = t.TypeVar("T3")

def mzip(*iterables: t.Iterable[t.Any], strict: bool = False) -> Mapper[tuple[t.Any, ...]]:
    return Mapper(zip(*iterables, strict=strict))

def mzip_longest(*iterables: t.Iterable[t.Any], fillvalue: t.Any = None) -> Mapper[tuple[t.Any, ...]]:
    return Mapper(zip_longest(*iterables, fillvalue=fillvalue))

def mrange(*args: int) -> Mapper[int]:
    return Mapper(range(*args))

# @t.overload
# def partial(func: t.Callable[[T, *Ts]], /, *args: P.args, **kwargs: P.kwargs) -> t.Callable[]: ...

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

partial = _p

def with_predicate(func: t.Callable[[T, G], T3]) -> t.Callable[[T], t.Callable[[G], T3]]:
    def get_predicate(predicate: T):
        def call(iterable: G):
            return func(predicate, iterable)
        return call
    return get_predicate

def with_rightargs(func: t.Callable[t.Concatenate[T, P], G]) -> t.Callable[P, t.Callable[[T], G]]:
    def get_rightargs(*args: P.args, **kwargs: P.kwargs) -> t.Callable[[T], G]:
        def call(iterable: T) -> G:
            return func(iterable, *args, **kwargs)
        return call
    return get_rightargs
