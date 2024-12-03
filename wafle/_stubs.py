"""Internally seperated utility functions
which need special attention to their typing information
"""

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


def mzip(
    *iterables: t.Iterable[t.Any], strict: bool = False
) -> Mapper[tuple[t.Any, ...]]:
    """The mapper equivalent to :func:`zip`, takes any number of iterables and
    creates a :class:`wafle.Mapper` yielding tuples which holds the result of all
    passed iterables

    Parameters
    ----------
    *iterables: :class:`t.Iterable`, variadic
        The iterables to be zipped.
    strict: :class:`bool`, optional, keyword-only
        If one of the iterables is exhausted before others then raise :class:`ValueError`, by default False

    Returns
    -------
    :class:`wafle.Mapper`[:class:`tuple`[:class:`t.Any`, ...]]
        The mapper over the zipped iterable
    """
    return Mapper(zip(*iterables, strict=strict))


def mzip_longest(
    *iterables: t.Iterable[t.Any], fillvalue: t.Any = None
) -> Mapper[tuple[t.Any, ...]]:
    """
    zips iterables and continue till the last one is exhausted, filling the missing values in tuples
    with the provided value. Wrapper over :func:`zip_longest`

    Parameters
    ----------
    fillvalue : :class:`t.Any`, optional, keyword-only
        The value to fill with if an iterator is exhausted, by default None

    Returns
    -------
    :class:`wafle.Mapper`[:class:`tuple`[:class:`t.Any`, ...]]
        The mapper over the zipped iterable
    """
    return Mapper(zip_longest(*iterables, fillvalue=fillvalue))


def mrange(*args: int) -> Mapper[int]:
    """Make a mapper which wraps :func:`range`

    Parametrs
    ---------
    \\*args: :type:`int`
        Passed as is to :func:`range`

    Returns
    -------
    :class:`Mapper` (``Mapper[int]``)
        A :class:`Mapper` wrapping the range object
    """
    return Mapper(range(*args))


# @t.overload
# def partial(func: t.Callable[[T, *Ts]], /, *args: P.args, **kwargs: P.kwargs) -> t.Callable[]: ...


def rpartial(func, /, *args, **keywords):
    """creates a partial where the supplied positional arguments
    are supplied as the right most positional arguments in ltr order

    Parameters
    ----------
    func : :type:`t.Callable`
        A callable object.

    Returns
    -------
    :type:`t.Callable`
        A callable object with the rightmos, keyword arguments applied
    """

    def newfunc(*fargs, **fkeywords):
        newkeywords = {**keywords, **fkeywords}
        return func(*fargs, *args, **newkeywords)

    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc


partial = _p


def with_predicate(
    func: t.Callable[[T, G], T3],
) -> t.Callable[[T], t.Callable[[G], T3]]:
    """Curry a function such that the first positional argument is passed during first call
    and the second argument during second call.

    Parameters
    ----------
    func : ``Callable[[T, G], T3]``
        The two argument function to be curried

    Returns
    -------
    ``Callable[[T], Callable[[G], T3]]``
        The curried function
    """

    def get_predicate(predicate: T):
        def call(iterable: G):
            return func(predicate, iterable)

        return call

    return get_predicate


def with_rightargs(
    func: t.Callable[t.Concatenate[T, P], G],
) -> t.Callable[P, t.Callable[[T], G]]:
    """Make a function such that the right arguments are supplied on the first call and
    the first positional argument is supplied on the second call

    Parameters
    ----------
    func : ``Callable[Concatenate[T, P], G]``
        The callable object

    Returns
    -------
    ``Callable[P,Callable[[T], G]]``
        The modified callable
    """

    def get_rightargs(*args: P.args, **kwargs: P.kwargs) -> t.Callable[[T], G]:
        def call(iterable: T) -> G:
            return func(iterable, *args, **kwargs)

        return call

    return get_rightargs
