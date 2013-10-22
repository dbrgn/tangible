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


### 3D shapes ###

def test_good_cube():
    try:
        cube = ast.Cube(2, 3, 4.5)
    except ValueError:
        pytest.fail()
    assert cube.width == 2
    assert cube.height == 3
    assert cube.depth == 4.5


@pytest.mark.parametrize(('width', 'height', 'depth'), [
    (0, 1, 1),  # zero width
    (1, 0, 1),  # zero height
    (1, 1, 0),  # zero depth
    (-1, 1, 1),  # negative width
    (1, -1, 1),  # negative height
    (1, 1, -1),  # negative depth
])
def test_bad_cube(width, height, depth):
    with pytest.raises(ValueError):
        ast.Cube(width, height, depth)


def test_good_sphere():
    try:
        sphere = ast.Sphere(5.5)
    except ValueError:
        pytest.fail()
    assert sphere.radius == 5.5


@pytest.mark.parametrize('radius', [
    0,  # zero radius
    -4.4,  # negative radius
])
def test_bad_sphere(radius):
    with pytest.raises(ValueError):
        ast.Sphere(radius)


def test_good_cylinder():
    try:
        cylinder = ast.Cylinder(10, 3, 5.5)
    except ValueError:
        pytest.fail()
    assert cylinder.height == 10
    assert cylinder.radius1 == 3
    assert cylinder.radius2 == 5.5


@pytest.mark.parametrize(('height', 'radius1', 'radius2'), [
    (0, 1, 1),  # zero height
    (1, 0, 1),  # zero radius1
    (1, 1, 0),  # zero radius2
    (-1, 1, 1),  # negative height
    (1, -1, 1),  # negative radius1
    (1, 1, -1),  # negative radius2
])
def test_bad_cylinder(height, radius1, radius2):
    with pytest.raises(ValueError):
        ast.Cylinder(height, radius1, radius2)


def test_good_polyhedron():
    try:
        points = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]
        triangles = [(0, 1, 2), (1, 0, 3), (1, 3, 2), (0, 2, 3)]
        polyhedron = ast.Polyhedron(points, triangles)
    except ValueError:
        pytest.fail()
    assert polyhedron.points == points
    assert polyhedron.triangles == triangles


def test_polyhedron_type():
    points = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]
    triangles = [(0, 1, 2), (1, 0, 3), (1, 3, 2), (0, 2, 3)]
    quads = [(0, 1, 2, 3)]
    polyhedron3 = ast.Polyhedron(points, triangles=triangles)
    polyhedron4 = ast.Polyhedron(points, quads=quads)
    assert polyhedron3.polygon_type == 'triangles'
    assert polyhedron4.polygon_type == 'quads'


@pytest.mark.parametrize(('points', 'triangles', 'quads'), [
    (  # Not enough points
        [(0, 0, 0), (1, 0, 0), (1, 1, 0)],
        [(0, 1, 2)], None
    ),
    (  # Both triangles and quads
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [(0, 1, 2)], [(0, 1, 2, 3)],
    ),
    (  # Neither triangles nor quads
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        None, None,
    ),
    (  # Invalid triangles
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [(0, 1, 2), (1, 0, 3, 4), (1, 3, 2), (0, 2, 3)], None
    ),
    (  # Invalid quads
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        None, [(0, 1, 2), (1, 0, 3, 4), (1, 3, 2), (0, 2, 3)]
    ),
    (  # Referenced invalid point in triangles (too large)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [(0, 1, 4), (1, 0, 3), (1, 3, 2), (0, 2, 3)], None
    ),
    (  # Referenced invalid point in triangles (negative)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [(0, 1, -1), (1, 0, 3), (1, 3, 2), (0, 2, 3)], None
    ),
    (  # Referenced invalid point in quads (too large)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        None, [(0, 1, 2, 4)]
    ),
    (  # Referenced invalid point in quads (negative)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        None, [(0, 1, 2, -1)]
    ),
])
def test_bad_polyhedron(points, triangles, quads):
    print(triangles)
    print(quads)
    with pytest.raises(ValueError):
        ast.Polyhedron(points, triangles, quads)
