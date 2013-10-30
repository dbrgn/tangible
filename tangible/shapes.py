# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import izip

from . import ast, utils


### BASE CLASS ###

class Shape(object):
    """The base class for all shapes.

    This class provides the base functionality to store data, build an `AST
    <ast.html>`_ and render it using the selected `backend <backends.html>`_.

    """
    def __init__(self, data):
        self.data = data

    def _build_ast(self):
        raise NotImplementedError('_build_ast method not implemented.')

    def render(self, backend):
        """Build the AST_ and generate code using the selected backend_.

        :param backend: The backend_ class used to process the AST_. Must accept
            the AST as constructor argument and provide a ``generate()`` method.
        :returns: The resulting source code as a string.

        """
        self.ast = self._build_ast()
        return backend(self.ast).generate()


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

class CircleTower1D(VerticalShape):
    """Round vertical tower. Datapoints are mapped to radius."""
    def _build_ast(self):
        layers = [ast.Circle(radius=d) for d in self.data]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class SquareTower1D(VerticalShape):
    """Vertical tower made of squares. Datapoints are mapped to square side length."""
    def _build_ast(self):
        layers = [ast.Rectangle(width=d, height=d) for d in self.data]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class RectangleTower2D(VerticalShape):
    """Vertical tower made of rectangles. Datapoints are mapped to width and
    height of rectangle."""
    def _build_ast(self):
        if len(self.data[0]) != len(self.data[1]):
            raise ValueError('Both datasets need to have the same length.')
        layers = [ast.Rectangle(width=a, height=b) for a, b in izip(*self.data)]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class RhombusTower2D(VerticalShape):
    """Vertical tower made of rhombi. Datapoints are mapped to distance between
    opposing corners."""
    def _build_ast(self):
        if len(self.data[0]) != len(self.data[1]):
            raise ValueError('Both datasets need to have the same length.')
        layers = []
        for a, b in izip(*self.data):
            rhombus = ast.Polygon([(0, a / 2), (b / 2, 0), (0, -a / 2), (-b / 2, 0), (0, a / 2)])
            layers.append(rhombus)
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


# TODO: PolygonTowerND


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
