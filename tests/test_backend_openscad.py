# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from tangible import ast
from tangible.backends.openscad import OpenScadBackend as Backend


def verify(shape, code):
    """Helper function."""
    assert Backend(shape).generate() == code


@pytest.mark.parametrize(('shape', 'code'), [
    (ast.Circle(radius=10), 'circle(10);'),
    (ast.Rectangle(width=1, height=2), 'square([1, 2]);'),
    (ast.Cube(width=1, height=2, depth=3), 'cube([1, 3, 2]);'),
    (ast.Sphere(radius=10), 'sphere(10);'),
    (ast.Cylinder(height=3, radius1=1, radius2=2), 'cylinder(3, 1, 2);'),
    (ast.Translate(1, 2, 3, ast.Circle(1)), 'translate([1, 2, 3])\n{\n    circle(1);\n};'),
    (ast.Rotate(30, (0, 1, 0), ast.Circle(1)), 'rotate(30, [0, 1, 0])\n{\n    circle(1);\n};'),
    (ast.Rotate(30, [0, 1, 0], ast.Circle(1)), 'rotate(30, [0, 1, 0])\n{\n    circle(1);\n};'),
    (ast.Mirror([0, 1, 1], ast.Circle(1)), 'mirror([0, 1, 1])\n{\n    circle(1);\n};'),
    (ast.Union([ast.Circle(1), ast.Sphere(2)]),
        'union()\n{\n    circle(1);\n    sphere(2);\n};'),
    (ast.Difference([ast.Circle(1), ast.Sphere(2)]),
        'difference()\n{\n    circle(1);\n    sphere(2);\n};'),
    (ast.Intersection([ast.Circle(1), ast.Sphere(2)]),
        'intersection()\n{\n    circle(1);\n    sphere(2);\n};'),
    (ast.LinearExtrusion(height=7, item=ast.Circle(1)),
        'linear_extrude(7, twist=0)\n{\n    circle(1);\n};'),
    (ast.LinearExtrusion(height=7, twist=90, item=ast.Circle(1)),
        'linear_extrude(7, twist=90)\n{\n    circle(1);\n};'),
    (ast.RotateExtrusion(ast.Circle(1)), 'rotate_extrude()\n{\n    circle(1);\n};'),
])
def test_simple_shapes(shape, code):
    verify(shape, code)


def test_polygon():
    shape = ast.Polygon(points=[(0, 0), (0, 2), (1, 2), (0, 0)])
    code = 'polygon([[0, 0], [0, 2], [1, 2]]);'
    verify(shape, code)


# TODO test_polyhedron
