# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible.shapes.pie import AnglePie1D
from tangible.backends.openscad import OpenScadBackend

datapoints = [10, 20, 30, 40, 50]
pie = AnglePie1D(datapoints, height=2, outer_radius=10, inner_radius=0, explode=0.2)
code = pie.render(backend=OpenScadBackend)
print(code)
