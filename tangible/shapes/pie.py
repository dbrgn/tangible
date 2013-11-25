# -*- coding: utf-8 -*-
"""Circular shapes."""
from __future__ import print_function, division, absolute_import, unicode_literals

from .. import ast
from .base import Shape
from .mixins import Data1DMixin, DataNDMixin, SameLengthDatasetMixin


### BASE CLASS ###

class PieShape(SameLengthDatasetMixin, Shape):
    """Base class for pie shapes."""
    def __init__(self, data, inner_radius=0):
        """
        """
        super(PieShape, self).__init__(data)
        self.inner_radius = inner_radius
        self.count = len(self.data[0])
        self.angles = [360 / self.count for i in self.data[0]]


### SHAPE CLASSES ###
