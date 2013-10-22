# -*- coding: utf-8 -*-
"""
AST module.

This module contains the building blocks for an abstract syntax tree (AST)
representation of 3D objects. It is implemented using namedtuples.

"""
from __future__ import print_function, division, absolute_import, unicode_literals

from collections import namedtuple

__VERSION__ = '1'


### Base class for AST types ###

class AST(object):
    """Base class for AST objects."""

    def __eq__(self, other):
        """This method override ensures that two objects are considered equal
        when their attributes match. Object identity is irrelevant."""
        return isinstance(other, self.__class__) \
            and self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Inverse of ``__eq__``."""
        return not self.__eq__(other)


### 2D shapes ###

class Circle(AST):
    """A circle 2D shape."""
    def __init__(self, radius):
        """
        :param radius: The radius of the circle.
        :type radius: int or float

        """
        if radius <= 0:
            raise ValueError('Radius of a circle must be > 0.')
        self.radius = radius


class Rectangle(AST):
    """A rectangle 2D shape."""
    def __init__(self, width, height):
        """
        :param width: Width of the rectangle.
        :type width: int or float
        :param width: Height of the rectangle.
        :type width: int or float

        """
        if width <= 0:
            raise ValueError('Width must be > 0.')
        if height <= 0:
            raise ValueError('Height must be > 0.')
        self.width = width
        self.height = height


class Polygon(AST):
    """A polygon 2D shape."""
    def __init__(self, points):
        """
        :param points: List of coordinates. Ordering is important. The shape
            must be closed, meaning that the first and the last coordinate must be
            the same.
        :type points: list of 2-tuples

        """
        if points[0] != points[-1]:
            raise ValueError('The shape must be closed, meaning that the first '
                             'and the last coordinate must be the same.')
        if len(points) < 4:
            raise ValueError('A polygon consists of at least 3 points.')
        self.points = points


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
