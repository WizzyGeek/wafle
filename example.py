import itertools as it
import typing as t

from wafle import M, mapper, mrange
import wafle as wf

print(M(range(10)).consume(sum))
print((mapper <= range(10)) >= sum)
print((range(10) >= mapper) >= sum)
print(mrange(10) >= sum)

print(mapper.of(range(4)) | (lambda x: x + 1) >= max)

_: t.Any = (
    mapper.of(range(1, 101))
    | (lambda x: ("Fizz" * (x % 3 == 0) + "Buzz" * (x % 5 == 0)) or str(x))
    | print
    >= list
)


_ = (
    wf.mrange(1, 101)
    | (lambda x: ("Fizz" * (x % 3 == 0) + "Buzz" * (x % 5 == 0)) or str(x))
    | print
)
wf.void(_)


# make partial islice to use conviniently
# I promised to add all typesafe itertools partials soon
islice = wf.with_rightargs(it.islice)  # type: ignore

_ = wf.M(input("Numbers: ").split()) | int > islice(None, None, 2)  # type: ignore
print(_ >= sum)
