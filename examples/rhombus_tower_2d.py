# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible import shapes
from tangible.backends.openscad import OpenScadBackend


datapoints = [
    [6, 10, 6],
    [6, 6, 22],
]


# Create shape
tower = shapes.RhombusTower2D(datapoints, layer_height=10)

code = tower.render(backend=OpenScadBackend)
print(code)
