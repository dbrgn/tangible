# -*- coding: utf-8 -*-
"""Vertical shapes."""
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import izip

from .. import ast, utils
from .base import Shape
from .mixins import Data1DMixin, Data2DMixin, Data4DMixin, SameLengthDatasetMixin


### BASE CLASS ###

class VerticalShape(Shape):
    """Base class for vertical shapes like towers.

    :param data: The data.
    :type data: sequence type
    :param layer_height: The height of each layer in the vertical shape.
    :type layer_height: int or float

    """
    def __init__(self, data, layer_height):
        super(VerticalShape, self).__init__(data)
        self.layer_height = layer_height


### SHAPE CLASSES ###

class CircleTower1D(Data1DMixin, VerticalShape):
    """Round vertical tower. Datapoints are mapped to radius."""
    def _build_ast(self):
        layers = [ast.Circle(radius=d) for d in self.data[0]]
        return utils.connect_2d_shapes(layers, self.layer_height, 'vertical')


class SquareTower1D(Data1DMixin, VerticalShape):
    """Vertical tower made of squares. Datapoints are mapped to square side length."""
    def _build_ast(self):
        layers = [ast.Rectangle(width=d, height=d) for d in self.data[0]]
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
