import typing as t
from . import Mapper as Mapper

T = t.TypeVar("T")
G = t.TypeVar("G")
P = t.ParamSpec("P")
T3 = t.TypeVar("T3")
T4 = t.TypeVar("T4")
Ts = t.TypeVarTuple("Ts")
Gs = t.TypeVarTuple("Gs")

@t.overload
def mzip(*, strict: bool = ...) -> Mapper[t.Any]: ...
@t.overload
def mzip(iter1: t.Iterable[T], *, strict: bool = ...) -> Mapper[tuple[T]]: ...
@t.overload
def mzip(
    iter1: t.Iterable[T], iter2: t.Iterable[G], *, strict: bool = ...
) -> Mapper[tuple[T, G]]: ...
@t.overload
def mzip(
    iter1: t.Iterable[T],
    iter2: t.Iterable[G],
    iter3: t.Iterable[T3],
    *,
    strict: bool = ...,
) -> Mapper[tuple[T, G, T3]]: ...
@t.overload
def mzip_longest(*, fillvalue: t.Any = ...) -> Mapper[t.Any]: ...
@t.overload
def mzip_longest(iter1: t.Iterable[T], *, fillvalue: T4) -> Mapper[tuple[T | T4]]: ...
@t.overload
def mzip_longest(
    iter1: t.Iterable[T], iter2: t.Iterable[G], *, fillvalue: T4
) -> Mapper[tuple[T | T4, G | T4]]: ...
@t.overload
def mzip_longest(
    iter1: t.Iterable[T], iter2: t.Iterable[G], iter3: t.Iterable[T3], *, fillvalue: T4
) -> Mapper[tuple[T | T4, G | T4, T3 | T4]]: ...
@t.overload
def mzip_longest(iter1: t.Iterable[T]) -> Mapper[tuple[T | None]]: ...
@t.overload
def mzip_longest(
    iter1: t.Iterable[T], iter2: t.Iterable[G]
) -> Mapper[tuple[T | None, G | None]]: ...
@t.overload
def mzip_longest(
    iter1: t.Iterable[T], iter2: t.Iterable[G], iter3: t.Iterable[T3]
) -> Mapper[tuple[T | None, G | None, T3 | None]]: ...
@t.overload
def mrange(stop: int) -> Mapper[int]: ...
@t.overload
def mrange(start: int, stop: int) -> Mapper[int]: ...
@t.overload
def mrange(start: int, stop: int, step: int) -> Mapper[int]: ...

class rpartial(t.Generic[*Ts, T]):
    # @t.overload
    # def __new__(
    #     cls, func: type[filter], arg1: t.Iterable[T], **kwargs
    # ) -> rpartial[t.Callable[[T], bool] | None, filter[T]]: ...  # type: ignore[overload-overlap]
    @t.overload  # Problematic for mypy
    def __new__(cls, func: t.Callable, /, *args, **kwargs) -> rpartial[*Ts, T]: ...  # type: ignore[overload-overlap]
    @t.overload
    def __new__(
        cls, func: t.Callable[[T3, G], T], arg1: G, **kwargs
    ) -> rpartial[T3, T]: ...
    @t.overload
    def __new__(
        cls, func: t.Callable[[T3, T4, G], T], arg1: G, **kwargs
    ) -> rpartial[T3, T4, T]: ...
    @t.overload
    def __new__(
        cls, func: t.Callable[[T3, T4, G], T], arg1: T4, arg2: G, **kwargs
    ) -> rpartial[T3, T]: ...
    @t.overload
    def __new__(
        cls, func: t.Callable[[*Ts, G], T], arg1: G, **kwargs
    ) -> rpartial[*Ts, T]: ...
    @t.overload
    def __new__(
        cls, func: t.Callable[[*Ts, G, T3], T], arg1: G, arg2: T3, **kwargs
    ) -> rpartial[*Ts, T]: ...
    @t.overload
    def __new__(
        cls,
        func: t.Callable[[*Ts, G, T3, T4], T],
        arg1: G,
        arg2: T3,
        args3: T4,
        **kwargs,
    ) -> rpartial[*Ts, T]: ...
    @staticmethod
    def __call__(*args: *Ts, **kwargs: t.Any) -> T: ...

class partial(t.Generic[*Ts, T]):
    # @t.overload
    # def __new__(cls, func: type[filter], arg1: t.Callable[[T], bool] | None, **kwargs) -> partial[[t.Iterable[T]], filter[T]]: ... # type: ignore[overload-overlap]
    @t.overload  # Problematic for mypy
    def __new__(cls, func: t.Callable, /, *args, **kwargs) -> rpartial[*Ts, T]: ...  # type: ignore[overload-overlap]
    @t.overload
    def __new__(
        cls, func: t.Callable[[T3, *Ts], T], arg1: T3, **kwargs
    ) -> partial[*Ts, T]: ...
    @t.overload
    def __new__(
        cls, func: t.Callable[[T3, T4, *Ts], T], arg1: T3, arg2: T4, **kwargs
    ) -> partial[*Ts, T]: ...
    @t.overload
    def __new__(
        cls,
        func: t.Callable[[T3, T4, G, *Ts], T],
        arg1: T3,
        arg2: T4,
        arg3: G,
        **kwargs,
    ) -> partial[*Ts, T]: ...
    @t.overload
    def __new__(cls, func: t.Callable[..., T], *args, **kwargs) -> partial[*Ts, T]: ...
    @staticmethod
    def __call__(*args: *Ts, **kwargs) -> T: ...

# partial = _p

# @t.overload
# def with_predicate(func: type[filter[T]]) -> partial[t.Callable[[T], bool] | None, partial[t.Iterable[T], filter[T]]]: ...
# @t.overload

class RCurried(t.Generic[T, G, T3]):
    def __new__(cls, arg1: T) -> t.Self: ...
    @staticmethod
    def __call__(arg2: G) -> T3: ...

def with_predicate(func: t.Callable[[T, G], T3]) -> type[RCurried[T, G, T3]]: ...

class VarCurried(t.Generic[T, P, T3]):
    def __new__(cls, *arg: P.args, **kwargs: P.kwargs) -> t.Self: ...
    @staticmethod
    def __call__(arg: T) -> T3: ...

def with_rightargs(func: t.Callable[t.Concatenate[T, P], G]) -> VarCurried[T, P, G]: ...
