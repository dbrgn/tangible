# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from tangible import scales


@pytest.mark.parametrize(('param', 'clamp', 'expected'), [
    # Regular values
    (2, False, 10),
    (3, False, 15),
    (3.5, False, 17.5),
    (4, False, 20),
    # Clamping
    (6, False, 30),
    (6, True, 20),
    (-1, False, -5),
    (-1, True, 10),
])
def test_linear(param, clamp, expected):
    """Test the linear scale."""
    domain = (2, 4)
    codomain = (10, 20)
    scale = scales.linear(domain, codomain, clamp)
    assert scale(param) == expected


@pytest.mark.parametrize(('param', 'clamp', 'expected'), [
    # Regular values
    (1, False, 20),
    (3, False, 10),
    (2.5, False, 12.5),
    # Clamping
    (0, False, 25),
    (0, True, 20),
    (7, False, -10),
    (7, True, 10),
])
def test_linear_inverted_codomain(param, clamp, expected):
    """Test the linear scale with inverted codomain."""
    domain = (1, 3)
    codomain = (20, 10)
    scale = scales.linear(domain, codomain, clamp)
    assert scale(param) == expected
