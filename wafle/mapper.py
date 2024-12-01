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
    """
    A single parameter callable which calls the wrapped callable with variable length positional argument.
    """

    func: t.Callable[..., G]

    def __init__(self, func: t.Callable[..., G]) -> None:
        """Initialise the Star object

        Parameters
        ----------
        func : :type:`t.Callable`[..., G]
            A callable oject
        """
        self.func = func

    def __call__(self, args: t.Iterable[t.Any]) -> G:
        """Call the wrapped callable

        Parameters
        ----------
        args : :type:`t.Iterable`[:type:`t.Any`]
            An iterable providing the positional arguments to be supplied.

        Returns
        -------
        The result of calling the wrapped callable
        """
        return self.func(*args)


star = Star
"""Alias of Star"""


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


# TODO: Move to metaclass
mapper = MapperFactory()
"""
A :class:`MapperFactory` object, It uses binary operations to make :class:`Mapper` objects from iterables.

Example
-------
.. code-block:: python

    print((mapper <= range(10)) >= sum)
    print((range(10) >= mapper) >= sum)
"""


class Mapper(t.Generic[T]):
    """
    An iterable whch wraps another iterable.
    """

    __slots__ = ("data",)
    data: t.Iterable[T]

    def __init__(self, iterable: t.Iterable[T]) -> None:
        """Initialize the mapper

        Parameters
        ----------
        iterable : :type:`t.Iterable`[T]
            An iterable
        """
        self.data = iterable

    def __or__(self, o: t.Callable[[T], G]) -> Mapper[G]:
        """Map given function over the mapper

        Parameters
        ----------
        o : ``Callable[[T], G]``
            A callable whch is used as the mapping function.

        Returns
        -------
        :class:`Mapper` (``Mapper[G]``)
            A new :class:`Mapper` which is in the return type of the mapping function
        """
        if callable(o):
            if isinstance(o, Star):
                return Mapper(starmap(o.func, self.data))  # type: ignore
            return Mapper(map(o, self.data))
        else:
            return NotImplemented

    __ior__ = __or__

    def __gt__(
        self, transformer: t.Callable[[t.Iterable[T]], t.Iterable[G]]
    ) -> Mapper[G]:
        """Applies a transformer to the mapper.

        Parameters
        ----------
        transformer : ``Callable[[Iterable[T]], Iterable[G]]``
            A callable which takes in one iterable and transforms it to return another

        Returns
        -------
        :class:`Mapper` (``Mapper[G]``)
            A new :class:`Mapper` wrapping the transformed iterable
        """
        if callable(transformer):
            return Mapper(transformer(self.data))
        else:
            return NotImplemented

    __matmul__ = __gt__
    __truediv__ = __or__

    def __ge__(self, consumer: t.Callable[[t.Iterable[T]], G]) -> G:
        """Feeds the mapper to the provided consumer

        Parameters
        ----------
        consumer : ``Callable[[Iterable[T]], G]``
            A callable which is a consumer of iterable.

        Returns
        -------
        The result of the consuming function
        """
        if callable(consumer):
            return consumer(self.data)
        else:
            return NotImplemented

    def apply(
        self,
        transformer: t.Callable[t.Concatenate[t.Iterable[T], P], t.Iterable[G]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Mapper[G]:
        """Call a transformer

        Parameters
        ----------
        transformer : :type:`t.Callable`[..., :type:`t.Iterable[G]`]
            A callable such that the first argument must be an iterable and the return type must also be an iterable.
        *args, **kwargs :
            Rest of the arguments are passed as is to the transforming function

        Returns
        -------
        :class:`Mapper` (``Mapper[G]``)
            :class:`Mapper` wrapping the transformed iterable.
        """
        return Mapper(transformer(self.data, *args, **kwargs))

    def consume(
        self,
        consumer: t.Callable[t.Concatenate[t.Iterable[T], P], G],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> G:
        """Feeds the mapper to the provided consumer

        Parameters
        ----------
        consumer : ``Callable[..., G]``
            A callable such that the first argument must be an iterable.
        *args, **kwargs :
            Rest of the arguments are passed as is to the consuming function

        Returns
        -------
        The result of the consuming function
        """
        return consumer(self.data, *args, **kwargs)

    @t.overload
    def reduce(self, reducer: t.Callable[[T, T], T]) -> T: ...

    @t.overload
    def reduce(self, reducer: t.Callable[[G, T], G], initialiser: G) -> G: ...

    def reduce(self, reducer, initialiser=_MISSING):
        """Apply a function of two arguments cumulatively to the items of the :class:`Mapper`,
        from left to right, so as to reduce the :class:`Mapper` to a single value

        Parameters
        ----------
        reducer : :type:`t.Callable`
            A binary callable
        initialiser : :type:`t.Any`, optional
            The intial value that is placed before all values in the :class:`Mapper`
            serves as a default value.

        Returns
        -------
        The result of the reducing function,
        """
        if initialiser is _MISSING:
            return _reduce(reducer, self)
        else:
            return _reduce(reducer, self, initialiser)

    def __iter__(self) -> t.Iterator[T]:
        return iter(self.data)

    def __bool__(self) -> bool:
        return bool(self.data)

    void = _void
    """Consumes the :class:`Mapper` entirely"""


# Alias
M = Mapper
"""Alias for :class:`Mapper`"""
