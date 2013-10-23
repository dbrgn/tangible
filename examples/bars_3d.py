# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import csv
from itertools import chain

from tangible import scales, shapes
from tangible.backends.openscad import OpenScadBackend


# Read data into list
datapoints = [list() for i in xrange(9)]
with open('analytics-full-13.csv', 'r') as datafile:
    reader = csv.DictReader(datafile)
    for row in reader:
        date = row['Day']
        month = int(date.split('/', 1)[0])
        visits = int(row['Visits'])
        datapoints[month - 1].append(visits)


# Normalize data
all_datapoints = list(chain.from_iterable(datapoints))
scale = scales.linear([min(all_datapoints), max(all_datapoints)], [10, 150])
datapoints = map(lambda x: map(scale, x), datapoints)


# Create shape
bars3d = shapes.Bars3D(datapoints, bar_width=7, bar_depth=7, center_layers=True)

code = bars3d.render(backend=OpenScadBackend)
print(code)
