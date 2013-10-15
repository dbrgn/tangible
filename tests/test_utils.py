# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from tangible import utils


@pytest.mark.parametrize(('values', 'pairs'), [
    (range(6), [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]),
    ([2, 4], [(2, 4)]),
    ([1], []),
])
def test_pairwise_list(values, pairs):
    assert list(utils.pairwise(values)) == pairs
