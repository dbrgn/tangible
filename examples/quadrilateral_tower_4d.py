# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible import shapes
from tangible.backends.openscad import OpenScadBackend


datapoints = [
    [10, 5, 10, 5, 10],
    [20, 16, 20, 16, 20],
    [5, 10, 5, 10, 5],
    [6, 8, 6, 8, 6],
]


# Create shape
tower = shapes.QuadrilateralTower4D(datapoints, layer_height=10)

code = tower.render(backend=OpenScadBackend)
print(code)
