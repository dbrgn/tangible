# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from tangible import shapes
from tangible.shapes.base import Shape


@pytest.mark.parametrize('data', [
    [1, 2, 3],
    (1, 2, 3),
    [[1, 2], [3, 4, 5], (6, 7)],
])
def test_valid_base_shape(data):
    try:
        Shape(data)
    except ValueError:
        pytest.fail()


@pytest.mark.parametrize('data', [
    '',
    None,
])
def test_invalid_base_shape(data):
    with pytest.raises(ValueError):
        Shape(data)


@pytest.mark.parametrize(('data', 'angle'), [
    (xrange(1), 360),
    (xrange(2), 180),
    (xrange(10), 36),
    (xrange(16), 22.5),
])
def test_base_pie(data, angle):
    my_pie = shapes.pie.PieShape(data)
    assert len(my_pie.angles) == len(data), "# of angles should equal # of datapoints."
    assert my_pie.angles[0] == angle, "Angle should be 360/len(datapoints)."
    assert len(set(my_pie.angles)) == 1, "All angles should be the same."
