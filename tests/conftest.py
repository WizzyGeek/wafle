import wafle as wf

import pytest


@pytest.fixture
def seq():
    return range(10)


@pytest.fixture
def mappr(seq):
    return wf.M(seq)
