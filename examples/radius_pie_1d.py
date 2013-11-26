# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible.shapes.pie import RadiusPie1D
from tangible.backends.openscad import OpenScadBackend

datapoints = [18, 23, 15, 20, 10]
pie = RadiusPie1D(datapoints, height=10, inner_radius=3)
code = pie.render(backend=OpenScadBackend)
print(code)
