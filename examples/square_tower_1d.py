# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import csv

from tangible import scales
from tangible.shapes.vertical import SquareTower1D
from tangible.backends.openscad import OpenScadBackend


# Read data into list
datapoints = []
with open('analytics-sep-13.csv', 'r') as datafile:
    reader = csv.DictReader(datafile)
    for row in reader:
        visits = int(row['Visits'])
        datapoints.append(visits)


# Normalize data
scale = scales.linear([min(datapoints), max(datapoints)], [10, 50])
datapoints = map(scale, datapoints)


# Create shape
tower = SquareTower1D(datapoints, layer_height=10)

code = tower.render(backend=OpenScadBackend)
print(code)
