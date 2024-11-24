from wafle import M, mapper, mrange

print(M(range(10)).consume(sum))
print((mapper <= range(10)) >= sum)
print((range(10) >= mapper) >= sum)
print(mrange(10) >= sum)

print(mapper.of(range(4)) | (lambda x: x + 1) >= max)

_ = mapper.of(range(1, 101)) | (lambda x: ("Fizz" * (x % 3 == 0) + "Buzz" * (x % 5 == 0)) or str(x)) | print >= list


import wafle as wf

_ = wf.mrange(1, 101)
_ |= lambda x: ("Fizz" * (x % 3 == 0) + "Buzz" * (x % 5 == 0)) or str(x)
wf.void(_ | print)

import itertools as it

# make partial islice to use conviniently
# I promised to add all typesafe itertools partials soon
islice = wf.with_rightargs(it.islice)

_ = wf.M(input("Numbers: ").split()) | int
_ = _ > islice(None, None, 2) # type: ignore
print(_ >= sum)