# -*- coding: utf-8 -*-
"""
AST module.

This module contains the building blocks for an abstract syntax tree (AST)
representation of 3D objects. It is implemented using namedtuples.

"""
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import chain

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

    def __repr__(self):
        name = self.__class__.__name__
        return '<AST/{0}: {1}>'.format(name, id(self))


### 2D shapes ###

class Circle(AST):
    """A circle 2D shape."""
    def __init__(self, radius):
        """
        :param radius: The radius of the circle.
        :type radius: int or float
        :raises: ValueError if validation fails.

        """
        if radius <= 0:
            raise ValueError('Radius of a circle must be > 0.')
        self.radius = radius


class CircleSector(Circle):
    """A circle sector (pizza slice)."""
    def __init__(self, radius, angle):
        """
        :param radius: The radius of the circle.
        :type radius: int or float
        :param angle: The central angle in degrees.
        :type angle: int or float
        :raises: ValueError if validation fails.

        """
        super(CircleSector, self).__init__(radius)
        if angle <= 0:
            raise ValueError('Angle must be > 0.')
        if angle > 360:
            raise ValueError('Angle must be between 0 and 360.')
        self.angle = angle


class Rectangle(AST):
    """A rectangle 2D shape."""
    def __init__(self, width, height):
        """
        :param width: Width of the rectangle.
        :type width: int or float
        :param height: Height of the rectangle.
        :type height: int or float
        :raises: ValueError if validation fails.

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
        :param points: List of coordinates. Order of points is significant. The
            shape must be closed, meaning that the first and the last coordinate
            must be the same.
        :type points: list of 2-tuples
        :raises: ValueError if validation fails.

        """
        if points[0] != points[-1]:
            raise ValueError('The shape must be closed, meaning that the first '
                             'and the last coordinate must be the same.')
        if len(points) < 4:
            raise ValueError('A polygon consists of at least 3 points.')
        self.points = points


# 3D shapes

class Cube(AST):
    """A cube 3D shape."""
    def __init__(self, width, height, depth):
        """
        :param width: Width of the cube.
        :type width: int or float
        :param height: Height of the cube.
        :type height: int or float
        :param depth: Depth of the cube.
        :type depth: int or float
        :raises: ValueError if validation fails.

        """
        if width <= 0:
            raise ValueError('Width must be > 0.')
        if height <= 0:
            raise ValueError('Height must be > 0.')
        if depth <= 0:
            raise ValueError('Depth must be > 0.')
        self.width = width
        self.height = height
        self.depth = depth


class Sphere(AST):
    """A sphere 3D shape."""
    def __init__(self, radius):
        """
        :param radius: The radius of the sphere.
        :type radius: int or float
        :raises: ValueError if validation fails.

        """
        if radius <= 0:
            raise ValueError('Radius of a sphere must be > 0.')
        self.radius = radius


class Cylinder(AST):
    """A cylinder 3D shape."""
    def __init__(self, height, radius1, radius2):
        """
        :param height: The height of the cylinder.
        :type height: int or float
        :param radius1: The bottom radius of the cylinder.
        :type radius1: int or float
        :param radius2: The top radius of the cylinder.
        :type radius2: int or float
        :raises: ValueError if validation fails.

        """
        if height <= 0:
            raise ValueError('Height of a cylinder must be > 0.')
        if radius1 <= 0:
            raise ValueError('Bottom radius (radius1) of a cylinder must be > 0.')
        if radius2 <= 0:
            raise ValueError('Top radius (radius2) of a cylinder must be > 0.')
        self.height = height
        self.radius1 = radius1
        self.radius2 = radius2


class Polyhedron(AST):
    """A polyhedron 3D shape. Supports both triangles and quads. Triangles and
    quads can also be mixed."""
    def __init__(self, points, triangles=[], quads=[]):
        """
        :param points: List of points.
        :type points: list of 3-tuples
        :param triangles: Triangles formed by a 3-tuple of point indexes (e.g.
            ``(0, 1, 3)``). When looking at the triangle from outside, the points
            must be in clockwise order. Default: ``[]``.
        :type triangles: list of 3-tuples
        :param quads: Rectangles formed by a 4-tuple of point indexes (e.g.
            ``(0, 1, 3, 4)``). When looking at the rectangle from outside, the
            points must be in clockwise order. Default: ``[]``.
        :type quads: list of 4-tuples
        :raises: ValueError if validation fails.

        """
        if len(points) < 4:
            raise ValueError('There must be at least 4 points in a polyhedron.')
        if set(map(len, points)) != set([3]):
            raise ValueError('Invalid point tuples (must be 3-tuples).')
        if not (triangles or quads):
            raise ValueError('Either triangles or quads must be specified.')
        if triangles:
            if set(map(len, triangles)) != set([3]):
                raise ValueError('Invalid triangle tuples (must be 3-tuples).')
        if quads:
            if set(map(len, quads)) != set([4]):
                raise ValueError('Invalid quad tuples (must be 4-tuples).')
        max_value = max(chain(*(triangles + quads)))
        min_value = min(chain(*(triangles + quads)))
        if max_value >= len(points):
            raise ValueError('Invalid point index: {}'.format(max_value))
        if min_value < 0:
            raise ValueError('Invalid point index: {}'.format(min_value))
        self.points = points
        self.triangles = triangles
        self.quads = quads


### Transformations ###

class Translate(AST):
    """A translate transformation."""
    def __init__(self, x, y, z, item):
        """
        :param x: Translation on the X axis.
        :type x: int or float
        :param y: Translation on the Y axis.
        :type y: int or float
        :param z: Translation on the Z axis.
        :type z: int or float
        :param item: An AST object.
        :type item: tangible.ast.AST
        :raises: ValueError if validation fails

        """
        if not item:
            raise ValueError('Item is required.')
        if not isinstance(item, AST):
            raise ValueError('Item must be an AST type.')
        self.x = x
        self.y = y
        self.z = z
        self.item = item


class Rotate(AST):
    """A rotate transformation."""
    def __init__(self, degrees, vector, item):
        """
        :param degrees: Number of degrees to rotate.
        :type degrees: int or float
        :param vector: The axes to rotate around. When a rotation is specified
            for multiple axes then the rotation is applied in the following
            order: x, y, z. As an example, a vector of [1,1,0] will cause the object
            to be first rotated around the x axis, and then around the y axis.
        :type y: 3-tuple
        :param item: An AST object.
        :type item: tangible.ast.AST
        :raises: ValueError if validation fails

        """
        if not item:
            raise ValueError('Item is required.')
        if not isinstance(item, AST):
            raise ValueError('Item must be an AST type.')
        if not len(vector) == 3:
            raise ValueError('Invalid vector (must be a 3-tuple).')
        if not any(vector):
            raise ValueError('Invalid vector (must contain at least one `1` value).')
        if set(vector) != set([0, 1]):
            raise ValueError('Invalid vector (must consist of `0` and `1` values).')
        self.degrees = degrees
        self.vector = vector
        self.item = item


class Scale(AST):
    """A scale transformation."""
    def __init__(self, x, y, z, item):
        """
        The x, y and z attributes are multiplicators of the corresponding
        dimensions. E.g. to double the height of an object, you'd use ``1, 1, 2``
        as x, y and z values.

        :param x: X axis multiplicator.
        :type x: int or float
        :param y: Y axis multiplicator.
        :type y: int or float
        :param z: Z axis multiplicator.
        :type z: int or float
        :param item: An AST object.
        :type item: tangible.ast.AST
        :raises: ValueError if validation fails

        """
        if not item:
            raise ValueError('Item is required.')
        if not isinstance(item, AST):
            raise ValueError('Item must be an AST type.')
        if 0 in [x, y, z]:
            raise ValueError('Values of 0 are not allowed in a scale transformation.')
        self.x = x
        self.y = y
        self.z = z
        self.item = item


class Mirror(AST):
    """A mirror transformation."""
    def __init__(self, vector, item):
        """
        Mirror the child element on a plane through the origin.

        :param vector: Normal vector describing the plane intersecting the
            origin through which to mirror the object.
        :type vector: 3-tuple
        :param item: An AST object.
        :type item: tangible.ast.AST
        :raises: ValueError if validation fails

        """
        if not item:
            raise ValueError('Item is required.')
        if not isinstance(item, AST):
            raise ValueError('Item must be an AST type.')
        if not len(vector) == 3:
            raise ValueError('Invalid vector (must be a 3-tuple).')
        if not any(vector):
            raise ValueError('Invalid vector (must contain at least one non-zero value).')
        self.vector = tuple(vector)
        self.item = item


### Boolean operations ###

class _BooleanOperation(AST):
    """Base class for boolean operations that only take the ``items`` argument."""
    def __init__(self, items):
        """
        :param items: List of AST objects.
        :type items: list
        :raises: ValueError if validation fails

        """
        if not items:
            raise ValueError('Items are required.')
        if not hasattr(items, '__iter__'):
            raise ValueError('Items must be iterable.')
        if len(items) < 2:
            raise ValueError('Union must contain at least 2 items.')
        if not all(map(lambda x: isinstance(x, AST), items)):
            raise ValueError('All items must be AST types.')
        self.items = items


class Union(_BooleanOperation):
    """A union operation."""
    pass


class Difference(_BooleanOperation):
    """A difference operation."""
    pass


class Intersection(_BooleanOperation):
    """A intersection operation."""
    pass


### Extrusions ###

class LinearExtrusion(AST):
    """A linear extrusion along the z axis."""
    def __init__(self, height, item, twist=0):
        """
        :param height: The height of the extrusion.
        :type height: int or float
        :param item: An AST object.
        :type item: tangible.ast.AST
        :param twist: How many degrees to twist the object around the z axis.
        :type twist: int or float

        """
        if not item:
            raise ValueError('Item is required.')
        if not isinstance(item, AST):
            raise ValueError('Item must be an AST type.')
        self.height = height
        self.item = item
        self.twist = twist


class RotateExtrusion(AST):
    """A rotational extrusion around the z axis."""
    def __init__(self, item):
        """
        :param item: An AST object.
        :type item: tangible.ast.AST

        """
        if not item:
            raise ValueError('Item is required.')
        if not isinstance(item, AST):
            raise ValueError('Item must be an AST type.')
        self.item = item
