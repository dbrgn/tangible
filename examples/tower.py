# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import csv

from tangible import scales
from tangible.shapes import Vertical2D


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

# Loop over datapoints, generate OpenSCAD code
height = 5
last_point = 10
print('union() {')
for i, point in enumerate(datapoints):
    print('\ttranslate([0, 0, %d]) { cylinder(%d, %d, %d, $fa=5); };'
            % (height * i, height, last_point, point))
    last_point = point
print('};')
