# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from tangible import ast


### Equality ###

def test_equality():
    """Equality should only compare attribute values, not identity."""
    c1 = ast.Circle(42)
    c2 = ast.Circle(42)
    assert c1 == c2


### 2D shapes ###

def test_good_circle():
    try:
        circle = ast.Circle(5.5)
    except ValueError:
        pytest.fail()
    assert circle.radius == 5.5


@pytest.mark.parametrize('radius', [
    0,  # zero radius
    -4.4,  # negative radius
])
def test_bad_circle(radius):
    with pytest.raises(ValueError):
        ast.Circle(radius)


def test_good_rectangle():
    try:
        rectangle = ast.Rectangle(2, 4.5)
    except ValueError:
        pytest.fail()
    assert rectangle.width == 2
    assert rectangle.height == 4.5


@pytest.mark.parametrize(('width', 'height'), [
    (0, 1),  # zero width
    (1, 0),  # zero height
    (-1, 1),  # negative width
    (1, -1),  # negative height
])
def test_bad_rectangle(width, height):
    with pytest.raises(ValueError):
        ast.Rectangle(width, height)


def test_good_polygon():
    points = [(0, 0), (0, 1), (1, 2), (2, 0), (0, 0)]
    try:
        polygon = ast.Polygon(points)
    except ValueError:
        pytest.fail()
    assert len(polygon.points) == 5


@pytest.mark.parametrize('points', [
    [(0, 0), (1, 0), (0, 0)],  # too small
    [(0, 0), (1, 0), (2, 3)],  # not closed
])
def test_bad_polygon(points):
    with pytest.raises(ValueError):
        ast.Polygon(points)
