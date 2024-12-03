import pytest
from wafle import mrange, mzip, mzip_longest, rpartial, with_predicate, with_rightargs

from itertools import accumulate


def test_mrange(mappr):
    assert (mappr >= sum) == (mrange(10) >= sum)


def test_mzip():
    a = mzip(range(10), range(10))
    a |= lambda k: k[0] + k[1]
    assert (a >= sum) == 90


def test_mzip_longest():
    a = mzip_longest(range(10), range(11), fillvalue=0)
    a |= lambda k: k[0] + k[1]
    assert (a >= sum) == 100


def test_rpartial():
    def foo(a, b, /, e, c, *, d):
        return a + (b << 2) + (c << 4) + (d << 6)

    assert rpartial(foo, 0)(1, 2, -1, d=3) == 0b11_00_10_01
    assert rpartial(foo, c=0)(1, 2, -1, d=3) == 0b11_00_10_01

    with pytest.raises(TypeError):
        rpartial(foo, b=0)(1, 2, d=3)


def test_wtih_predicate():
    cf = with_predicate(filter)
    odd = cf(lambda k: k % 2)  # type: ignore

    assert sum(odd(range(10))) == 25  # type: ignore

    with pytest.raises(TypeError):
        cf(lambda k: 1, b=3)  # type: ignore
        odd(range(1), c="3")  # type: ignore


def test_wtih_rightargs():
    acc = with_rightargs(accumulate)
    acc = acc(lambda a, b: a + b)  # type: ignore

    assert sum(acc(range(10))) == 165  # type: ignore
