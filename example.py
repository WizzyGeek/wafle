from wafle import M, mapper, mrange

print(M(range(10)).consume(sum))
print((mapper <= range(10)) >= sum)
print((range(10) >= mapper) >= sum)
print(mrange(10) >= (lambda x: sum(x)))

print(mapper.of(range(4)) | (lambda x: x + 1) >= max)

_ = mapper.of(range(1, 101)) | (lambda x: ("Fizz" * (x % 3 == 0) + "Buzz" * (x % 5 == 0)) or str(x)) | print >= list