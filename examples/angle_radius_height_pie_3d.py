# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible.shapes.pie import AngleRadiusHeightPie3D
from tangible.backends.openscad import OpenScadBackend

datapoints = [
    [30, 30, 5, 5, 20],  # Angle
    [18, 23, 15, 20, 10],  # Radius
    [10, 20, 30, 25, 40],  # Height
]
pie = AngleRadiusHeightPie3D(datapoints)
code = pie.render(backend=OpenScadBackend)
print(code)
