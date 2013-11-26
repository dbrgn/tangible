# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible.shapes.pie import RadiusHeightPie2D
from tangible.backends.openscad import OpenScadBackend

datapoints = [
    [18, 23, 15, 20, 10],
    [10, 20, 30, 25, 40],
]
pie = RadiusHeightPie2D(datapoints)
code = pie.render(backend=OpenScadBackend)
print(code)
