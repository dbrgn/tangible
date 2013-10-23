# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from . import ast, utils


### BASE CLASS ###

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
        :returns: The resulting source code as a string.

        """
        self.ast = self._build_ast()
        return backend(self.ast).render()


### MAIN SHAPE TYPES ###

class VerticalShape(Shape):
    """Base class for vertical shapes like towers.

    :param data: The data.
    :type data: list
    :param layer_height: The height of each layer in the vertical shape.
    :type layer_height: int or float

    """
    def __init__(self, data, layer_height):
        super(VerticalShape, self).__init__(data)
        self.layer_height = layer_height


class BarsShape(Shape):
    """Base class for vertical bars.

    :param data: The data.
    :type data: list
    :param bar_width: The width of each bar.
    :type bar_width: int or float
    :param bar_depth: The depth of each bar.
    :type bar_depth: int or float

    """
    def __init__(self, data, bar_width, bar_depth):
        super(BarsShape, self).__init__(data)
        self.bar_width = bar_width
        self.bar_depth = bar_depth


### CUSTOM SHAPES ###

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
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


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


class Bars2D(BarsShape):
    """Vertical bars aligned next to each other horizontally. Datapoints are
    mapped to bar height."""
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


class Bars3D(BarsShape):
    """Vertical bars aligned next to each other horizontally. Datapoints are
    mapped to bar height. Multiple layers of bars."""
    def __init__(self, data, bar_width, bar_depth, center_layers=False):
        super(Bars3D, self).__init__(data, bar_width, bar_depth)
        self.center_layers = center_layers

    def _build_ast(self):
        layers = []
        for i, month in enumerate(self.data):
            bars2d = Bars2D(month, self.bar_width, self.bar_depth)
            layer = bars2d._build_ast()
            if not self.center_layers:
                layer = layer.item
            x_offset = (i % 2) * 0.1  # Used to prevent "invalid 2-manifold" error
            translated = ast.Translate(x=x_offset, y=i * self.bar_depth, z=0, item=layer)
            layers.append(translated)
        model = ast.Union(items=layers)
        # Center model
        #x_offset =
        y_offset = len(self.data) / 2 * self.bar_depth
        return ast.Translate(x=0, y=-y_offset, z=0, item=model)
