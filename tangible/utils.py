# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import tee, izip


def pairwise(iterable):
    """Iterate over an iterable in pairs.

    This is an implementation of a moving window over an iterable with 2 items.
    Each group in the resulting list contains 2 items.  This means that the
    original iterable needs to contain at least 2 items, otherwise this
    function will return an empty list.

    Example::

        [1, 2, 3, 4] -> [(1, 2), (2, 3), (3, 4)]

    :param iterable: An iterable containing at least 2 items.
    :type iterable: Any iterable type (e.g. a list or a tuple).
    :returns: A generator returning pairwise items.
    :rtype: :class:`itertools.izip`

    """
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
