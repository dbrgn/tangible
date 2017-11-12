#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import re
import inspect
import subprocess

from tangible import shapes


# Get all shape classes
pred = lambda c: inspect.isclass(c) and issubclass(c, shapes.base.Shape)
vertical_classes = inspect.getmembers(shapes.vertical, pred)
bars_classes = inspect.getmembers(shapes.bars, pred)
pie_classes = inspect.getmembers(shapes.pie, pred)
classes = vertical_classes + bars_classes + pie_classes


# Get names of shape classes
shape_names = [c[0] for c in classes]


# Transform shape names
def convert(name):
    s = name
    for i in range(4):
        s = re.sub('([^_])([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([0-9]+)([A-Za-z]+)', r'_\1\2', s).lower()
file_names = map(convert, shape_names)


# Find and execute files
for name in file_names:
    print('Processing {0}.py: '.format(name), end='')
    cmds = [
        'python {0}.py > {0}.scad',
        'openscad -o ../docs/_static/img/shapes/{0}.png --imgsize=400,260 {0}.scad',
        'rm {0}.scad',
    ]
    try:
        with open(os.devnull, 'w') as devnull:
            for cmd in cmds:
                subprocess.check_call(cmd.format(name), shell=True, stderr=devnull)
        print('OK')
    except:
        print('Failed')
