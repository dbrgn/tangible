# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import csv

import numpy as np
from tangible.shapes import Vertical2D


# Read data into list
datapoints = []
with open('analytics-sep-13.csv', 'r') as datafile:
    reader = csv.DictReader(datafile)
    for row in reader:
        datapoints.append(row['Visits'])

# Normalize data
