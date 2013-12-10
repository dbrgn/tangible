# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals


def _clamp(value, domain):
    """
    Clamp function. Limits the value to the given domain.

    (TODO: Maybe rewriting this using ``numpy.clip`` would make it faster?)

    :param value: The value to clamp.
    :param domain: A 2-tuple with the domain to clamp to.
    :returns: The value, clamped to the specified domain.

    """
    return sorted((domain[0], value, domain[1]))[1]


def linear(domain, codomain, clamp=False):
    """
    Return a function to linearly scale the values in the ``domain`` range to
    values in the ``codomain`` range.

    :param domain: The scale's input domain.
    :type domain: A 2-tuple.
    :param codomain: The scale's output range / codomain.
    :type codomain: A 2-tuple.
    :param clamp: Whether or not to clamp the output values to the codomain.
    Default ``False``.
    :type clamp: bool
    :returns: A function that takes a single number as argument and returns
        another number.

    """
    d, c = domain, codomain  # Short aliases
    d_size = d[1] - d[0]
    c_size = c[1] - c[0]

    def scale(x):
        value = (c_size / d_size) * (x - d[0]) + c[0]
        return _clamp(value, codomain) if clamp is True else value

    return scale
