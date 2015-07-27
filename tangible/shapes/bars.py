# -*- coding: utf-8 -*-
"""Bar shapes."""
from __future__ import print_function, division, absolute_import, unicode_literals

from .. import ast
from .base import Shape
from .mixins import Data1DMixin, DataNDMixin


### BASE CLASS ###

class BarsShape(Shape):
    """Base class for vertical bars.

    :param data: The data.
    :type data: sequence type
    :param bar_width: The width of each bar.
    :type bar_width: int or float
    :param bar_depth: The depth of each bar.
    :type bar_depth: int or float

    """
    def __init__(self, data, bar_width, bar_depth):
        super(BarsShape, self).__init__(data)
        self.bar_width = bar_width
        self.bar_depth = bar_depth


### SHAPE CLASSES ###

class Bars1D(Data1DMixin, BarsShape):
    """Vertical bars aligned next to each other horizontally. Datapoints are
    mapped to bar height."""
    def _build_ast(self):
        bars = []
        for i, datapoint in enumerate(self.data[0]):
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
        """
        :param center_layers: Whether or not to center the layers
            horizontally (default False).
        :type center_layers: bool

        """
        super(BarsND, self).__init__(data, bar_width, bar_depth)
        self.center_layers = center_layers

    def _build_ast(self):
        layers = []
        for i, month in enumerate(self.data):
            bars1d = Bars1D(month, self.bar_width, self.bar_depth)
            layer = bars1d._build_ast()
            if not self.center_layers:
                layer = layer.item

            # Hack: Used to prevent "invalid 2-manifold" error
            # TODO: should probably be in backend
            x_offset = (i % 2) * 0.1

            translated = ast.Translate(x=x_offset, y=i * self.bar_depth, z=0, item=layer)
            layers.append(translated)
        model = ast.Union(items=layers)

        # Center model
        # x_offset = TODO
        y_offset = len(self.data) / 2 * self.bar_depth

        return ast.Translate(x=0, y=-y_offset, z=0, item=model)
