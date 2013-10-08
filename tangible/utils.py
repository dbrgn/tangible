# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import tee, izip


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
