# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible.shapes.pie import AngleRadiusPie2D
from tangible.backends.openscad import OpenScadBackend

datapoints = [
    [30, 30, 5, 5, 20],
    [18, 23, 15, 20, 10],
]
pie = AngleRadiusPie2D(datapoints, height=2, inner_radius=2)
code = pie.render(backend=OpenScadBackend)
print(code)
