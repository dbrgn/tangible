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
