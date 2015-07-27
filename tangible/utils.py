# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import tee, izip

from .ast import Circle, Rectangle, Polygon, Cylinder, Polyhedron, Union, Rotate, Translate


def pairwise(iterable):
    """Iterate over an iterable in pairs.

    This is an implementation of a moving window over an iterable with 2 items.
    Each group in the resulting list contains 2 items. This means that the
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


def reduceby(iterable, keyfunc, reducefunc, init):
    """Combination of ``itertools.groupby()`` and  ``reduce()``.

    This generator iterates over the iterable. The values are reduced using
    ``reducefunc`` and ``init`` as long as ``keyfunc(item)`` returns the same
    value.

    A possible use case would be to aggregate website visits and to group them
    by month. The corresponding SQL statement would be::

        SELECT SUM(visit_count) FROM visits GROUP BY month;

    Example::

        >>> keyfunc = lambda x: x % 2 == 0
        >>> reducefunc = lambda x, y: x + y
        >>> values = [1, 3, 5, 6, 8, 11]
        >>> groups = utils.reduceby(values, keyfunc, reducefunc, 0)
        >>> groups
        <generator object reduceby at 0xedc5a0>
        >>> list(groups)
        [9, 14, 11]

    :param iterable: An iterable to reduce. The iterable should be presorted.
    :param keyfunc: A key function. It should return the same value for all
        items belonging to the same group.
    :param reducefunc: The reduce function.
    :param init: The initial value for the reduction.
    :returns: A generator returning the reduced groups.
    :rtype: generator

    """
    first = True
    oldkey = None
    accum_value = init
    for i in iter(iterable):
        key = keyfunc(i)
        if first:
            oldkey = key
            first = False
        elif key != oldkey:
            yield accum_value
            accum_value = init
            oldkey = key
        accum_value = reducefunc(accum_value, i)
    yield accum_value


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

            quads = [
                # Bottom
                [0, 1, 2, 3],
                # Top
                [4, 7, 6, 5],
                # Sides
                [0, 4, 5, 1], [1, 5, 6, 2], [2, 6, 7, 3], [3, 7, 4, 0],
            ]

            layer = Polyhedron(points=points, quads=quads)

        # Polygon
        # Implemented by joining polyhedra.
        elif isinstance(first, Polygon):
            if len(first.points) != len(second.points):
                raise ValueError('All polygons need to have the same number of points.')

            vertice_count = len(first.points) - 1

            points = []
            for point in first.points[:-1]:
                points.append(list(point) + [0])
            for point in second.points[:-1]:
                points.append(list(point) + [layer_distance])

            triangles = []
            quads = []
            for j in xrange(vertice_count):
                # Sides
                quads.append([
                    (j + 1) % vertice_count,  # lower right
                    j,  # lower left
                    vertice_count + j,  # upper left
                    vertice_count + (j + 1) % vertice_count  # upper right
                ])
                if j >= 2 and j < vertice_count:
                    # Bottom
                    triangles.append([0, j - 1, j])
                    # Top
                    triangles.append([vertice_count + j, vertice_count + j - 1, vertice_count])

            layer = Polyhedron(points=points, quads=quads, triangles=triangles)

        else:
            raise ValueError('Unsupported shape: {!r}'.format(first))

        layers.append(Translate(0, 0, i * layer_distance, item=layer))
    union = Union(items=layers)
    if orientation == 'horizontal':
        return Rotate(degrees=90, vector=[0, 1, 0], item=union)
    return union


def _quads_to_triangles(quads):
    """Convert a list of quads to a list of triangles.

    :param quads: The list of quads.
    :type quads: list of 4-tuples
    :returns: List of triangles.
    :rtype: list of 3-tuples

    """
    triangles = []
    for quad in quads:
        triangles.append((quad[0], quad[1], quad[2]))
        triangles.append((quad[0], quad[2], quad[3]))
    return triangles


def _ensure_list_of_lists(data):
    """Ensure the data object is a list of lists.

    If it doesn't contain lists or tuples, wrap it in a list.

    :param data: The dataset.
    :type data: list or tuple
    :returns: Processed data.
    :rtype: list of lists
    :raises: ValueError if data is not a sequence type.

    """
    if not hasattr(data, '__iter__'):
        raise ValueError('Data must be a sequence type (e.g. a list)')
    if not data:
        return [[]]
    if hasattr(data[0], '__iter__'):
        return data
    return [data]
