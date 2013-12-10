# -*- coding: utf-8 -*-
"""Circular shapes."""
from __future__ import print_function, division, absolute_import, unicode_literals

from math import sin, cos, radians
from itertools import izip

from .. import ast, scales
from .base import Shape
from .mixins import SameLengthDatasetMixin, Data1DMixin, Data2DMixin, Data3DMixin


### BASE CLASS ###

class PieShape(SameLengthDatasetMixin, Shape):
    """Base class for pie shapes.

    :param data: The data.
    :type data: sequence type
    :param height: The height of the model (default 2).
    :type height: int or float
    :param outer_radius: The outer radius of the model (default 10).
    :type outer_radius: int or float
    :param inner_radius: The inner radius of the model (default 0).
    :type inner_radius: int or float
    :param explode: By how much to explode the sectors (default 0).
    :type explode: int or float

    """
    def __init__(self, data, height=2, outer_radius=10, inner_radius=0, explode=0):
        super(PieShape, self).__init__(data)
        self.inner_radius = inner_radius
        self.count = len(self.data[0])
        self.radii = [outer_radius] * self.count
        self.angles = [360 / self.count] * self.count
        self.heights = [height] * self.count
        self.explode = explode

    def _build_ast(self):
        slices = []
        total_angle = 0
        for i, (radius, angle, height) in enumerate(izip(self.radii, self.angles, self.heights)):
            # Create slice
            s = ast.CircleSector(radius, angle)
            # Explode
            if self.explode:
                x_offset = self.explode * sin(radians(angle / 2))
                y_offset = self.explode * cos(radians(angle / 2))
                s = ast.Translate(x_offset, y_offset, 0, s)
            # Rotate
            s = ast.Rotate(-total_angle, (0, 0, 1), s)
            total_angle += angle
            # Extrude
            s = ast.LinearExtrusion(height, s)
            slices.append(s)
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

class AnglePie1D(Data1DMixin, AngleMixin, PieShape):
    """A classical pie chart. The datapoints are mapped to the angles of the slices.

    Note that you won't be able to differentiate the slices without setting a
    positive ``explode`` value.

    """
    def __init__(self, data, height=2, outer_radius=10, inner_radius=0, explode=0):
        """
        :param data: The data.
        :type data: sequence type
        :param height: The height of the model (default 2).
        :type height: int or float
        :param outer_radius: The outer radius of the model (default 10).
        :type outer_radius: int or float
        :param inner_radius: The inner radius of the model (default 0).
        :type inner_radius: int or float
        :param explode: By how much to explode the sectors (default 0).
        :type explode: int or float

        """
        super(AnglePie1D, self).__init__(data, height=height,
                outer_radius=outer_radius, inner_radius=inner_radius,
                explode=explode)


class RadiusPie1D(Data1DMixin, RadiusMixin, PieShape):
    """A flat pie chart where the datapoints are mapped to the radius of the
    slices."""
    def __init__(self, data, height=2, inner_radius=0, explode=0):
        """
        :param data: The data.
        :type data: sequence type
        :param height: The height of the model (default 2).
        :type height: int or float
        :param inner_radius: The inner radius of the model (default 0).
        :type inner_radius: int or float
        :param explode: By how much to explode the sectors (default 0).
        :type explode: int or float

        """
        super(RadiusPie1D, self).__init__(data, height=height,
                inner_radius=inner_radius, explode=explode)


class HeightPie1D(Data1DMixin, HeightMixin, PieShape):
    """A pie chart where the datapoints are mapped to the height of the
    slices."""
    def __init__(self, data, outer_radius=10, inner_radius=0, explode=0):
        """
        :param data: The data.
        :type data: sequence type
        :param outer_radius: The outer radius of the model (default 10).
        :type outer_radius: int or float
        :param inner_radius: The inner radius of the model (default 0).
        :type inner_radius: int or float
        :param explode: By how much to explode the sectors (default 0).
        :type explode: int or float

        """
        super(HeightPie1D, self).__init__(data,
                outer_radius=outer_radius, inner_radius=inner_radius, explode=explode)


class AngleRadiusPie2D(Data2DMixin, AngleMixin, RadiusMixin, PieShape):
    """A flat pie chart where the two datasets correspond to the angle and the
    radius of the slices."""
    def __init__(self, data, height, angle_index=0, radius_index=1, inner_radius=0, explode=0):
        """
        :param data: The data.
        :type data: sequence type
        :param height: The height of the model (default 2).
        :type height: int or float
        :param angle_index: The index of the angle dataset (default 0).
        :type angle_index: int
        :param radius_index: The index of the radius dataset (default 1).
        :type radius_index: int
        :param inner_radius: The inner radius of the model (default 0).
        :type inner_radius: int or float
        :param explode: By how much to explode the sectors (default 0).
        :type explode: int or float

        """
        super(AngleRadiusPie2D, self).__init__(data, height=height,
                inner_radius=inner_radius, explode=explode,
                angle_index=angle_index, radius_index=radius_index)


class AngleHeightPie2D(Data2DMixin, AngleMixin, HeightMixin, PieShape):
    """A pie chart where the two datasets correspond to the angle and the
    height of the slices."""
    def __init__(self, data, angle_index=0, height_index=1, outer_radius=10, inner_radius=0,
                 explode=0):
        """
        :param data: The data.
        :type data: sequence type
        :param angle_index: The index of the angle dataset (default 0).
        :type angle_index: int
        :param height_index: The index of the height dataset (default 1).
        :type height_index: int
        :param outer_radius: The outer radius of the model (default 10).
        :type outer_radius: int or float
        :param inner_radius: The inner radius of the model (default 0).
        :type inner_radius: int or float
        :param explode: By how much to explode the sectors (default 0).
        :type explode: int or float

        """
        super(AngleHeightPie2D, self).__init__(data,
                outer_radius=outer_radius, inner_radius=inner_radius, explode=explode,
                angle_index=angle_index, height_index=height_index)


class RadiusHeightPie2D(Data2DMixin, RadiusMixin, HeightMixin, PieShape):
    """A pie chart where the two datasets correspond to the radius and the
    height of the slices."""
    def __init__(self, data, radius_index=0, height_index=1, inner_radius=0, explode=0):
        """
        :param data: The data.
        :type data: sequence type
        :param radius_index: The index of the radius dataset (default 0).
        :type radius_index: int
        :param height_index: The index of the height dataset (default 1).
        :type height_index: int
        :param inner_radius: The inner radius of the model (default 0).
        :type inner_radius: int or float
        :param explode: By how much to explode the sectors (default 0).
        :type explode: int or float

        """
        super(RadiusHeightPie2D, self).__init__(data,
                inner_radius=inner_radius, explode=explode,
                radius_index=radius_index, height_index=height_index)


class AngleRadiusHeightPie3D(Data3DMixin, AngleMixin, RadiusMixin, HeightMixin, PieShape):
    """A pie chart where the three datasets correspond to the angle, the radius
    and the height of the slices."""
    def __init__(self, data, angle_index=0, radius_index=1, height_index=2, inner_radius=0,
                 explode=0):
        """
        :param data: The data.
        :type data: sequence type
        :param angle_index: The index of the angle dataset (default 0).
        :type angle_index: int
        :param radius_index: The index of the radius dataset (default 1).
        :type radius_index: int
        :param height_index: The index of the height dataset (default 2).
        :type height_index: int
        :param inner_radius: The inner radius of the model (default 0).
        :type inner_radius: int or float
        :param explode: By how much to explode the sectors (default 0).
        :type explode: int or float

        """
        super(AngleRadiusHeightPie3D, self).__init__(data,
                inner_radius=inner_radius, explode=explode,
                angle_index=angle_index, radius_index=radius_index, height_index=height_index)
