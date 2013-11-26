# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible.shapes.pie import HeightPie1D
from tangible.backends.openscad import OpenScadBackend

datapoints = [10, 20, 30, 40, 50]
pie = HeightPie1D(datapoints, outer_radius=10, inner_radius=6)
code = pie.render(backend=OpenScadBackend)
print(code)
