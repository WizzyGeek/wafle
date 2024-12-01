======
Wafle
======

.. image:: ./../../.github/assets/banner.svg
    :width: 100%
    :alt: Wafle, Fast. Elegant. Concise
    :align: center

Let's speak Python before English 😎
------------------------------------

.. code-block:: python

    import wafle as wf

    (
        wf.mrange(1, 101)
        | (lambda x: ("Fizz" * (x % 3 == 0) + "Buzz" * (x % 5 == 0)) or str(x))
        | print
    ).void()


Not convinced? good job! cause I wouldn't be either, You must be thinking "that's just
a simple fizzbuzz which doesn't use any partials" right?

If you thought that you would be right, However the solution is in the same sentence,
using partials!

You may think that is unnecessary complexity, more thinking, but the more general idea
behind partials, currying has been around for a long time. You have to try it to get
hooked to it.

Here is some real code from `Advent of Code 2023 Day 18 <https://adventofcode.com/2023/day/18>`_


.. code-block:: python

    # AOC23 Day 18 Part 2 input parsing
    from wafle import mapper, star, rpartial
    import operator as op

    dl = [1j, 1+0j, -1j, -1+0j]

    a = mapper.of(open("day18/input.txt", "r").readlines()) | str.strip | str.split | rpartial(op.getitem, 2) | rpartial(op.getitem, slice(2, -1)) | (lambda k: dl[int(k[-1])] * int(k[:-1], 16))


WAFLE was created after AoC Day 17, so the usage you are looking at is the very very first
version

If you have a problem with writing out `rpartial` or `partial` you can always alias the
imports.

Here's some more short examples

.. code-block:: python

    import wafle as wf

    print(wf.mrange(int(input("Enter a number: "))) >= sum)


.. code-block:: python

    import wafle as wf
    import itertools as it

    # make partial islice to use conviniently
    # I promised to add all typesafe itertools partials soon
    islice = wf.with_rightargs(it.islice)  # type: ignore

    _ = wf.M(input("Numbers: ").split()) | int > islice(None, None, 2)  # type: ignore
    print(_ >= sum)

Wafle Design Goals
------------------
- Minimal overhead
- **Zero iteration overhead**
- Concise syntax
- Intuitive usage
- Compatibility with other iterator tools and some other abstractions
- Ability to produce one-liners for most transformations over data
- Type-safe
- IDE support, no black magic and remain statically analyzab
- Interoperability, WAFLE even tries to be compatible with its alternatives


Contents
--------

.. toctree::
    :maxdepth: 2

    api/index

.. autosummary:
..     :toctree:
..     :caption: API Summary

..    wafle

.. include:: wafle.rst