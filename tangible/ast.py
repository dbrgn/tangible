# -*- coding: utf-8 -*-
"""
AST module.

This module contains the building blocks for an abstract syntax tree (AST)
representation of 3D objects. It is implemented using namedtuples.

"""
from __future__ import print_function, division, absolute_import, unicode_literals

from collections import namedtuple

__VERSION__ = '1'


# 2D shapes
Circle = namedtuple('Circle', 'radius')
Rectangle = namedtuple('Rectangle', 'width heigh')
Polygon = namedtuple('Polygon', 'points paths')

# 3D shapes
Cube = namedtuple('Cube', 'width height depth')
Sphere = namedtuple('Sphere', 'radius')
Cylinder = namedtuple('Cylinder', 'height radius1 radius2')
Polyhedron = namedtuple('Polyhedron', 'points triangles')

# Transformations
Translate = namedtuple('Translate', 'x y z item')
Rotate = namedtuple('Rotate', 'degrees vector item')
Scale = namedtuple('Scale', 'x y z item')
Mirror = namedtuple('Mirror', 'x y z item')

# Boolean operations
Union = namedtuple('Union', 'items')
Difference = namedtuple('Difference', 'items')
Intersection = namedtuple('Intersection', 'items')

# Extrusions
LinearExtrusion = namedtuple('LinearExtrusion', 'height')
RotateExtrusion = namedtuple('RotateExtrusion', 'twist')
