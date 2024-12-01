"""
A simple functional programming utility library for python
"""

from __future__ import annotations

from ._stubs import (
    mrange,
    rpartial,
    mzip,
    mzip_longest,
    with_predicate,
    with_rightargs,
    partial,
)
from .consumers import void
from .mapper import Star, star, M, Mapper, mapper


__all__ = (
    "Star",
    "star",
    "M",
    "Mapper",
    "mapper",
    "mrange",
    "rpartial",
    "partial",
    "mzip",
    "mzip_longest",
    "with_predicate",
    "with_rightargs",
    "void",
)
