from wafle import mapper, Mapper, M, partial, Star


def test_factory(seq):
    a = (
        mapper.of(seq),
        Mapper(seq),
        M(seq),
        mapper <= seq,
        seq >= mapper,
        seq @ mapper,
        mapper @ seq,
    )

    for i in a:
        assert i.data == range(10)


def test_mapper_consume(mappr):
    assert (mappr >= list) == list(range(10))
    assert (mappr.consume(list)) == list(range(10))


def test_mapper_or(mappr):
    a = mappr | (lambda k: None)
    assert len(a >= list) == 10


def test_mapper_truediv(mappr):
    a = mappr / (lambda k: None)
    assert len(a >= list) == 10


def test_mapper_ior(mappr):
    mappr |= lambda k: k + 1

    assert len(mappr >= list) == 10


def test_mapper_transform(mappr):
    f = partial(filter, lambda k: k % 2)
    a = mappr.apply(f) >= sum
    b = (mappr > f) >= sum
    c = (mappr @ f) >= sum

    assert a == 25
    assert b == 25
    assert c == 25


def test_starmap(mappr):
    mappr |= lambda k: (k,)
    mappr |= Star(lambda k: k)
    assert (mappr >= sum) == 45


def test_void(mappr):
    mappr = mappr.apply(iter)
    mappr.void()

    assert len(mappr >= list) == 0


def test_reduce(mappr):
    assert mappr.reduce(lambda a, b: a + b) == 45

    mappr = mappr.apply(iter)
    mappr.void()
    assert mappr.reduce(lambda a, b: a + b, -827) == -827
