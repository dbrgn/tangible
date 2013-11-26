# -*- coding: utf-8 -*-
"""Circular shapes."""
from __future__ import print_function, division, absolute_import, unicode_literals

from itertools import izip

from .. import ast, scales
from .base import Shape
from .mixins import Data1DMixin, DataNDMixin, SameLengthDatasetMixin


### BASE CLASS ###

class PieShape(SameLengthDatasetMixin, Shape):
    """Base class for pie shapes."""
    def __init__(self, data, height=2, outer_radius=10, inner_radius=0):
        """
        """
        super(PieShape, self).__init__(data)
        self.inner_radius = inner_radius
        self.count = len(self.data[0])
        self.radii = [outer_radius] * self.count
        self.angles = [360 / self.count] * self.count
        self.heights = [height] * self.count

    def _build_ast(self):
        slices = []
        total_angle = 0
        for i, (radius, angle, height) in enumerate(izip(self.radii, self.angles, self.heights)):
            # Create slice
            s = ast.CircleSector(radius, angle)
            # Rotate
            total_angle += angle
            rotated = ast.Rotate(total_angle, (0, 0, 1), s)
            # Extrude
            extruded = ast.LinearExtrusion(height, rotated)
            slices.append(extruded)
        union = ast.Union(slices)
        if self.inner_radius:
            r = self.inner_radius
            center = ast.Cylinder(max(self.heights), r, r)
            return ast.Difference([union, center])
        return union


### MIXINS ###

class AngleMixin(object):
    """Use datapoint as angle."""
    def __init__(self, *args, **kwargs):
        index = kwargs.pop('angle_index', 0)
        super(AngleMixin, self).__init__(*args, **kwargs)
        data = self.data[index]
        scale = scales.linear([0, sum(data)], [0, 360])
        for i in xrange(self.count):
            self.angles[i] = scale(data[i])


class RadiusMixin(object):
    """Use datapoint as outer radius."""
    def __init__(self, *args, **kwargs):
        index = kwargs.pop('radius_index', 0)
        super(RadiusMixin, self).__init__(*args, **kwargs)
        data = self.data[index]
        self.radii = data


class HeightMixin(object):
    """Use datapoint as height."""
    def __init__(self, *args, **kwargs):
        index = kwargs.pop('height_index', 0)
        super(HeightMixin, self).__init__(*args, **kwargs)
        data = self.data[index]
        self.heights = data


### SHAPE CLASSES ###

class RadiusPie1D(RadiusMixin, PieShape):
    def __init__(self, data, height, inner_radius=0):
        super(RadiusPie1D, self).__init__(data, height=height,
                inner_radius=inner_radius)


class AnglePie1D(AngleMixin, PieShape):
    def __init__(self, data, height, outer_radius=1, inner_radius=0):
        super(AnglePie1D, self).__init__(data, height=height,
                outer_radius=outer_radius, inner_radius=inner_radius)


class AngleRadiusPie2D(AngleMixin, RadiusMixin, PieShape):
    def __init__(self, data, height, angle_index=0, radius_index=1, inner_radius=0):
        super(AngleRadiusPie2D, self).__init__(data, height=height,
                inner_radius=inner_radius, angle_index=angle_index,
                radius_index=radius_index)
