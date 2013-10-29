# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import tee, izip

from .ast import Circle, Rectangle, Polygon, Cylinder, Polyhedron, Union, Rotate, Translate


def pairwise(iterable):
    """Iterate over an iterable in pairs.

    This is an implementation of a moving window over an iterable with 2 items.
    Each group in the resulting list contains 2 items.  This means that the
    original iterable needs to contain at least 2 items, otherwise this
    function will return an empty list.

    Example::

        [1, 2, 3, 4] -> [(1, 2), (2, 3), (3, 4)]

    :param iterable: An iterable containing at least 2 items.
    :type iterable: Any iterable type (e.g. a list or a tuple).
    :returns: A generator returning pairwise items.
    :rtype: :class:`itertools.izip`

    """
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def quads_to_triangles(quads):
    """Convert a list of quads to a list of triangles.

    :param quads: The list of quads.
    :type quads: list of 4-tuples
    :returns: List of triangles.
    :rtype: list of 3-tuples

    """
    triangles = []
    for quad in quads:
        triangles.append([quad[0], quad[1], quad[2]])
        triangles.append([quad[0], quad[2], quad[3]])
    return triangles


def connect_2d_shapes(shapes, layer_distance, orientation):
    """Convert a list of 2D shapes to a 3D shape.

    Take a list of 2D shapes and create a 3D shape from it. Each layer is
    separated by the specified layer distance.

    :param shapes: List of shapes.
    :type shapes: Each shape in the list should be an AST object.
    :param layer_distance: The distance between two layers.
    :type layer_distance: int or float
    :param orientation: Either 'horizontal' or 'vertical'
    :type orientation: str or unicode
    :returns: :class:`ast.Union`

    """
    assert orientation in ['horizontal', 'vertical'], \
            '`orientation` argument must be either "horizontal" or "vertical".'
    layers = []
    for i, (first, second) in enumerate(pairwise(shapes)):

        layer = None

        # Validate type
        if type(first) != type(second):
            raise NotImplementedError('Joining different shape types is not currently supported.')

        # Circle
        # Implemented by joining cylinders.
        if isinstance(first, Circle):
            r1, r2 = first.radius, second.radius
            layer = Cylinder(height=layer_distance, radius1=r1, radius2=r2)

        # Rectangle
        # Implemented by joining polyhedra.
        elif isinstance(first, Rectangle):
            w1, h1 = first.width, first.height
            w2, h2 = second.width, second.height

            def get_layer_points(x, y, z):
                return [
                    [x / 2, y / 2, z],
                    [-x / 2, y / 2, z],
                    [-x / 2, -y / 2, z],
                    [x / 2, -y / 2, z],
                ]

            points = []
            points.extend(get_layer_points(w1, h1, 0))
            points.extend(get_layer_points(w2, h2, layer_distance))

            triangles = [
                # Bottom
                [0, 1, 3], [1, 2, 3],
                # Top
                [4, 6, 5], [4, 7, 6],
                # Sides
                [3, 2, 7], [2, 6, 7],
                [0, 3, 4], [3, 7, 4],
                [1, 0, 5], [0, 4, 5],
                [2, 1, 6], [1, 5, 6],
            ]

            layer = Polyhedron(points=points, triangles=triangles)

        # Polygon
        # Implemented by joining polyhedra.
        elif isinstance(first, Polygon):
            raise NotImplementedError('Not yet implemented.')

        layers.append(Translate(0, 0, i * layer_distance, item=layer))
    union = Union(items=layers)
    if orientation == 'horizontal':
        return Rotate(degrees=90, vector=[0, 1, 0], item=union)
    return union
