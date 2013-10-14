# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from . import ast, utils


class Tower(object):

    def __init__(self, data, layer_height):
        self.data = data
        self.layer_height = layer_height

    def _build_ast(self):
        layers = []
        for i, (lower, upper) in enumerate(utils.pairwise(self.data)):
            layer = ast.Cylinder(height=self.layer_height, radius1=lower, radius2=upper)
            translated_layer = ast.Translate(x=0, y=0, z=i * self.layer_height, item=layer)
            layers.append(translated_layer)
        return ast.Union(items=layers)

    def render(self, backend):
        self.ast = self._build_ast()
        return backend(self.ast).render()


class Bars2D(object):

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
