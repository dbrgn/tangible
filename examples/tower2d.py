# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import csv

from tangible import scales, shapes
from tangible.backends.openscad import OpenScadBackend


def parse_duration(string):
    """Parse duration string (hh:mm:ss). Return seconds as integer."""
    parts = map(int, string.split(':'))
    return 3600 * int(parts[0]) + 60 * parts[1] + parts[2]


# Read data into list
datapoints = [[], []]
with open('analytics-sep-13.csv', 'r') as datafile:
    reader = csv.DictReader(datafile)
    for row in reader:
        datapoints[0].append(int(row['Visits']))
        datapoints[1].append(parse_duration(row['AvgDuration']))

# Normalize data
for i, dataset in enumerate(datapoints):
    scale = scales.linear([min(dataset), max(dataset)], [10, 80])
    datapoints[i] = map(scale, dataset)


# Create shape
tower2d = shapes.Tower2D(datapoints, layer_height=10)


code = tower2d.render(backend=OpenScadBackend)
print(code)
