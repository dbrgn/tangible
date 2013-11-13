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
        quads = [(0, 1, 2, 3)]
        ast.Polyhedron(points, triangles=triangles)
        ast.Polyhedron(points, quads=quads)
        polyhedron = ast.Polyhedron(points, quads=quads, triangles=triangles)
    except ValueError:
        pytest.fail()
    assert polyhedron.points == points
    assert polyhedron.triangles == triangles
    assert polyhedron.quads == quads


@pytest.mark.parametrize(('points', 'triangles', 'quads'), [
    (  # Not enough points
        [(0, 0, 0), (1, 0, 0), (1, 1, 0)],
        [(0, 1, 2)], []
    ),
    (  # Neither triangles nor quads
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [], [],
    ),
    (  # Invalid triangles
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [(0, 1, 2), (1, 0, 3, 4), (1, 3, 2), (0, 2, 3)], []
    ),
    (  # Invalid quads
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [], [(0, 1, 2), (1, 0, 3, 4), (1, 3, 2), (0, 2, 3)]
    ),
    (  # Referenced invalid point in triangles (too large)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [(0, 1, 4), (1, 0, 3), (1, 3, 2), (0, 2, 3)], []
    ),
    (  # Referenced invalid point in triangles (negative)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [(0, 1, -1), (1, 0, 3), (1, 3, 2), (0, 2, 3)], []
    ),
    (  # Referenced invalid point in quads (too large)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [], [(0, 1, 2, 4)]
    ),
    (  # Referenced invalid point in quads (too large)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [(0, 1, 2), (0, 1, 3)], [(0, 1, 2, 4)]
    ),
    (  # Referenced invalid point in quads (negative)
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
        [], [(0, 1, 2, -1)]
    ),
])
def test_bad_polyhedron(points, triangles, quads):
    print(triangles)
    print(quads)
    with pytest.raises(ValueError):
        ast.Polyhedron(points, triangles, quads)


### Transformations ###

def test_good_translate():
    circle = ast.Circle(5.5)
    try:
        translate = ast.Translate(x=1, y=-0.5, z=0, item=circle)
    except ValueError:
        pytest.fail()
    assert translate.x == 1
    assert translate.y == -0.5
    assert translate.z == 0
    assert translate.item == circle


@pytest.mark.parametrize(('x', 'y', 'z', 'item'), [
    (1, 0, 1, None),  # no item
    (1, 0, 1, 'item'),  # non-AST item
    (1, 0, 1, []),  # non-AST item
])
def test_bad_translate(x, y, z, item):
    with pytest.raises(ValueError):
        ast.Translate(x, y, z, item)


def test_good_rotate():
    circle = ast.Circle(5.5)
    try:
        rotate = ast.Rotate(90, (1, 0, 0), item=circle)
    except ValueError:
        pytest.fail()
    assert rotate.degrees == 90
    assert rotate.vector == (1, 0, 0)


@pytest.mark.parametrize(('degrees', 'vector', 'item'), [
    (30, (1, 0, 0), None),  # no item
    (30, (1, 0, 0), 'item'),  # non-AST item
    (30, '1, 0, 0', ast.Circle(1)),  # invalid vector
    (30, (1, 0), ast.Circle(1)),  # invalid vector
    (30, (0, 0, 0), ast.Circle(1)),  # invalid vector
    (30, (2, 0, 0), ast.Circle(1)),  # invalid vector
    (30, (0.5, 0, 0), ast.Circle(1)),  # invalid vector
])
def test_bad_rotate(degrees, vector, item):
    with pytest.raises(ValueError):
        ast.Rotate(degrees, vector, item)


def test_good_scale():
    cylinder = ast.Cylinder(10, 2, 2)
    try:
        scale = ast.Scale(x=1, y=0.5, z=2, item=cylinder)
    except ValueError:
        pytest.fail()
    assert scale.x == 1
    assert scale.y == 0.5
    assert scale.z == 2
    assert scale.item == cylinder


@pytest.mark.parametrize(('x', 'y', 'z', 'item'), [
    (1, 0.5, 2, None),  # no item
    (1, 0.5, 2, 'item'),  # non-AST item
    (1, 1, 0, ast.Cylinder(10, 2, 2)),  # zero z value
])
def test_bad_scale(x, y, z, item):
    with pytest.raises(ValueError):
        ast.Scale(x, y, z, item)


def test_good_mirror():
    cylinder = ast.Cylinder(10, 2, 2)
    try:
        mirror = ast.Mirror([1, 0.5, 2], item=cylinder)
    except ValueError:
        pytest.fail()
    assert mirror.vector == (1, 0.5, 2)
    assert mirror.item == cylinder


@pytest.mark.parametrize(('vector', 'item'), [
    ([1, 1, 0], None),  # no item
    ([1, 1, 0], 'item'),  # non-AST item
    ([0, 0, 0], ast.Sphere(1)),  # invalid vector
])
def test_bad_mirror(vector, item):
    with pytest.raises(ValueError):
        ast.Mirror(vector, item)


### Boolean operations ###

@pytest.mark.parametrize('Cls', [ast.Union, ast.Difference, ast.Intersection])
def test_good_boolean(Cls):
    circle1 = ast.Circle(5.5)
    circle2 = ast.Circle(2)
    try:
        result = Cls(items=[circle1, circle2])
    except ValueError:
        pytest.fail()
    assert len(result.items) == 2
    assert result.items[0] == circle1


@pytest.mark.parametrize('Cls', [ast.Union, ast.Difference, ast.Intersection])
@pytest.mark.parametrize('items', [
    [],  # empty list
    1,  # non-iterable
    [ast.Circle(5)],  # only 1 item
    [ast.Circle(5), 2, 3],  # non-AST items
])
def test_bad_boolean(Cls, items):
    with pytest.raises(ValueError):
        Cls(items)


### Extrusions ###

def test_good_linear_extrusion():
    try:
        linear_extrusion = ast.LinearExtrusion(10, ast.Circle(3))
    except ValueError:
        pytest.fail()
    assert linear_extrusion.height == 10
    assert linear_extrusion.item.radius == 3


@pytest.mark.parametrize('item', [
    None,  # no item
    'foo',  # non-AST item
])
def test_bad_linear_extrusion(item):
    with pytest.raises(ValueError):
        ast.LinearExtrusion(10, item)


def test_good_rotate_extrusion():
    try:
        rotate_extrusion = ast.RotateExtrusion(ast.Circle(3))
    except ValueError:
        pytest.fail()
    assert rotate_extrusion.item.radius == 3


@pytest.mark.parametrize('item', [
    None,  # no item
    'foo',  # non-AST item
])
def test_bad_rotate_extrusion(item):
    with pytest.raises(ValueError):
        ast.RotateExtrusion(item)
