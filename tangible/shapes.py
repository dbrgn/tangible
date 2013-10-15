# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import izip

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


class Tower2D(object):

    def __init__(self, data, layer_height):
        self.data = data
        self.layer_height = layer_height

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
