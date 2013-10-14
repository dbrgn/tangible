# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import csv

from tangible import scales, shapes
from tangible.backends.openscad import OpenScadBackend


# Read data into list
datapoints = []
with open('analytics-sep-13.csv', 'r') as datafile:
    reader = csv.DictReader(datafile)
    for row in reader:
        visits = int(row['Visits'])
        datapoints.append(visits)


# Normalize data
scale = scales.linear([min(datapoints), max(datapoints)], [10, 80])
datapoints = map(scale, datapoints)


# Create shape
bars2d = shapes.Bars2D(datapoints, bar_width=10, bar_depth=10)

code = bars2d.render(backend=OpenScadBackend)
print(code)
