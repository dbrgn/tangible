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
        if not hasattr(data, '__iter__'):
            raise ValueError('Data must be a sequence type (e.g. a list)')

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


### MIXINS ###

class Data1DMixin(object):
    """Validate 1 dimensional data."""
    def __init__(self, data, *args, **kwargs):
        if not len(data):
            raise ValueError('Data must not be empty.')
        super(Data1DMixin, self).__init__(data, *args, **kwargs)


class Data2DMixin(object):
    """Validate 2 dimensional data."""
    def __init__(self, data, *args, **kwargs):
        if len(data) != 2:
            msg = 'Data must be 2-dimensional, but it contains {} datasets.'
            raise ValueError(msg.format(len(data)))
        super(Data2DMixin, self).__init__(data, *args, **kwargs)


class Data4DMixin(object):
    """Validate 4 dimensional data."""
    def __init__(self, data, *args, **kwargs):
        if len(data) != 4:
            msg = 'Data must be 4-dimensional, but it contains {} datasets.'
            raise ValueError(msg.format(len(data)))
        super(Data4DMixin, self).__init__(data, *args, **kwargs)


class DataNDMixin(object):
    """Validate n dimensional data."""
    def __init__(self, data, *args, **kwargs):
        if not len(data):
            raise ValueError('Data must not be empty.')
        if not all(map(lambda x: hasattr(x, '__iter__'), data)):
            raise ValueError('All data items must be a sequence type (e.g. a list).')
        super(DataNDMixin, self).__init__(data, *args, **kwargs)


class SameLengthDatasetMixin(object):
    """Make sure that each dataset in multi dimensional data has the same
    length."""
    def __init__(self, data, *args, **kwargs):
        if len(data) < 2:
            raise ValueError('Data must contain at least 2 datasets.')
        lengths = map(len, data)
        if len(set(lengths)) != 1:
            raise ValueError('All datasets in data must be of the same length.')
        super(SameLengthDatasetMixin, self).__init__(data, *args, **kwargs)


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

class CircleTower1D(Data1DMixin, VerticalShape):
    """Round vertical tower. Datapoints are mapped to radius."""
    def _build_ast(self):
        layers = [ast.Circle(radius=d) for d in self.data]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class SquareTower1D(Data1DMixin, VerticalShape):
    """Vertical tower made of squares. Datapoints are mapped to square side length."""
    def _build_ast(self):
        layers = [ast.Rectangle(width=d, height=d) for d in self.data]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class RectangleTower2D(Data2DMixin, SameLengthDatasetMixin, VerticalShape):
    """Vertical tower made of rectangles. Datapoints are mapped to width and
    height of rectangle."""
    def _build_ast(self):
        layers = [ast.Rectangle(width=a, height=b) for a, b in izip(*self.data)]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class RhombusTower2D(Data2DMixin, SameLengthDatasetMixin, VerticalShape):
    """Vertical tower made of rhombi. Datapoints are mapped to distance between
    opposing corners."""
    def _build_ast(self):
        layers = []
        for a, b in izip(*self.data):
            rhombus = ast.Polygon([(0, a / 2), (b / 2, 0), (0, -a / 2), (-b / 2, 0), (0, a / 2)])
            layers.append(rhombus)
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class QuadrilateralTower4D(Data4DMixin, SameLengthDatasetMixin, VerticalShape):
    """Vertical tower made of quadrilaterals (polygons with 4 vertices).
    Datapoints are mapped to distance between center and the corners."""
    def _build_ast(self):
        layers = []
        for a, b, c, d in izip(*self.data):
            quadrilateral = ast.Polygon([(0, a), (b, 0), (0, -c), (-d, 0), (0, a)])
            layers.append(quadrilateral)
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


# TODO: PolygonTowerND


class Bars1D(Data1DMixin, BarsShape):
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


class BarsND(DataNDMixin, BarsShape):
    """Vertical bars aligned next to each other horizontally. Datapoints are
    mapped to bar height. Multiple layers of bars (matching number of
    datasets)."""
    def __init__(self, data, bar_width, bar_depth, center_layers=False):
        super(BarsND, self).__init__(data, bar_width, bar_depth)
        self.center_layers = center_layers

    def _build_ast(self):
        layers = []
        for i, month in enumerate(self.data):
            bars1d = Bars1D(month, self.bar_width, self.bar_depth)
            layer = bars1d._build_ast()
            if not self.center_layers:
                layer = layer.item
            x_offset = (i % 2) * 0.1  # Hack: Used to prevent "invalid 2-manifold" error
                                      # TODO: should probably be in backend
            translated = ast.Translate(x=x_offset, y=i * self.bar_depth, z=0, item=layer)
            layers.append(translated)
        model = ast.Union(items=layers)
        # Center model
        #x_offset = TODO
        y_offset = len(self.data) / 2 * self.bar_depth
        return ast.Translate(x=0, y=-y_offset, z=0, item=model)
