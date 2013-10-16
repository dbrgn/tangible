# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from . import ast, utils


class Shape(object):
    """The base class for all shapes.

    This class provides the base functionality to store data, build an AST and
    render it using the selected backend.

    """
    def __init__(self, data):
        self.data = data

    def _build_ast(self):
        raise NotImplementedError('_build_ast method not implemented.')

    def render(self, backend):
        """Build the AST and render it using the selected backend.

        :param backend: The backend class used to render the AST. Must accept
            the AST as constructor argument and provide a ``render()`` method.
        :returns: The rendered AST as a string.

        """
        self.ast = self._build_ast()
        return backend(self.ast).render()


class VerticalShape(Shape):
    """Base class for vertical shapes.

    It adds the ``layer_height`` parameter to the constructor.

    """
    def __init__(self, data, layer_height):
        super(VerticalShape, self).__init__(data)
        self.layer_height = layer_height


class Tower(VerticalShape):
    """Round vertical tower. Datapoints are mapped to radius."""
    def _build_ast(self):
        layers = [ast.Circle(radius=d) for d in self.data]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class RectangularTower(VerticalShape):
    """Vertical tower with squares as layers. Datapoints are mapped to width/height."""
    def _build_ast(self):
        layers = [ast.Rectangle(d, d) for d in self.data]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class RectangularTower2D(VerticalShape):
    """Vertical tower with 4-sided polygons as layers. Datapoints are mapped to
    distance between opposing corners."""
    def _build_ast(self):
        layers = [ast.Rectangle(d1, d2) for d1, d2 in self.data]
        return utils.connect_2d_shapes(layers, self.layer_height, 'horizontal')


class Tower2D(VerticalShape):

    def _build_ast(self):
        layers = []
        for i in range(len(self.data[0]) - 1):
            lower1 = self.data[0][i]
            lower2 = self.data[1][i]
            upper1 = self.data[0][i + 1]
            upper2 = self.data[1][i + 1]
            z = i * self.layer_height
            points = [
                # Lower layer
                (lower1, 0, z),
                (0, lower2, z),
                (-lower1, 0, z),
                (0, -lower2, z),
                # Upper layer
                (upper1, 0, z + self.layer_height),
                (0, upper2, z + self.layer_height),
                (-upper1, 0, z + self.layer_height),
                (0, -upper2, z + self.layer_height),
            ]
            triangles = [
                # Bottom triangles
                (0, 1, 3),
                (1, 2, 3),
                # Top triangles
                (4, 7, 5),
                (5, 7, 6),
                # Sides
                (0, 7, 4),
                (0, 3, 7),
                (1, 4, 5),
                (1, 0, 4),
                (2, 5, 6),
                (2, 1, 5),
                (3, 6, 7),
                (3, 2, 6),
            ]
            layer = ast.Polyhedron(points, triangles)
            layers.append(layer)
        return ast.Union(items=layers)


class Bars2D(object):
    """Vertical bars aligned next to each other horizontally. Datapoints are
    mapped to bar height."""
    def __init__(self, data, bar_width, bar_depth):
        self.data = data
        self.bar_width = bar_width
        self.bar_depth = bar_depth

    def _build_ast(self):
        bars = []
        for i, datapoint in enumerate(self.data):
            bar = ast.Cube(width=self.bar_width, height=datapoint, depth=self.bar_depth)
            translated_bar = ast.Translate(x=i * self.bar_width, y=0, z=0, item=bar)
            bars.append(translated_bar)
        model = ast.Union(items=bars)
        # Center model
        x_offset = len(self.data) / 2 * self.bar_width
        return ast.Translate(x=-x_offset, y=0, z=0, item=model)

    def render(self, backend):
        self.ast = self._build_ast()
        return backend(self.ast).render()
