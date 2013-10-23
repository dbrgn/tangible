# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from tangible import utils, ast


@pytest.mark.parametrize(('values', 'pairs'), [
    (range(6), [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]),
    ([2, 4], [(2, 4)]),
    ([1], []),
])
def test_pairwise_list(values, pairs):
    assert list(utils.pairwise(values)) == pairs


class TestCircleConnect(object):

    @classmethod
    def setup_class(cls):
        cls.shapes = [
            ast.Circle(3),
            ast.Circle(8),
            ast.Circle(5),
        ]
        cls.union = ast.Union(items=[
            ast.Translate(0, 0, 0, ast.Cylinder(10, 3, 8)),
            ast.Translate(0, 0, 10, ast.Cylinder(10, 8, 5)),
        ])

    def test_vertical(self):
        result = utils.connect_2d_shapes(self.shapes, 10, 'vertical')
        assert result == self.union

    def test_horizontal(self):
        result = utils.connect_2d_shapes(self.shapes, 10, 'horizontal')
        vector = [0, 1, 0]
        assert result == ast.Rotate(90, vector, self.union)


class TestRectangleConnect(object):

    @classmethod
    def setup_class(cls):
        cls.shapes = [
            ast.Rectangle(width=6, height=6),
            ast.Rectangle(width=10, height=6),
            ast.Rectangle(width=6, height=22),
        ]
        cls.union = ast.Union(items=[
            ast.Translate(0, 0, 0,
                ast.Polyhedron(points=[
                    [3.0, 3.0, 0], [-3.0, 3.0, 0], [-3.0, -3.0, 0], [3.0, -3.0, 0],
                    [5.0, 3.0, 10], [-5.0, 3.0, 10], [-5.0, -3.0, 10], [5.0, -3.0, 10],
                ], triangles=[
                    [0, 1, 3], [1, 2, 3], [4, 6, 5], [4, 7, 6],
                    [3, 2, 7], [2, 6, 7], [0, 3, 4], [3, 7, 4],
                    [1, 0, 5], [0, 4, 5], [2, 1, 6], [1, 5, 6],
                ])
            ),
            ast.Translate(0, 0, 10,
                ast.Polyhedron(points=[
                    [5.0, 3.0, 0], [-5.0, 3.0, 0], [-5.0, -3.0, 0], [5.0, -3.0, 0],
                    [3.0, 11.0, 10], [-3.0, 11.0, 10], [-3.0, -11.0, 10], [3.0, -11.0, 10],
                ], triangles=[
                    [0, 1, 3], [1, 2, 3], [4, 6, 5], [4, 7, 6],
                    [3, 2, 7], [2, 6, 7], [0, 3, 4], [3, 7, 4],
                    [1, 0, 5], [0, 4, 5], [2, 1, 6], [1, 5, 6],
                ])
            ),
        ])

    def test_vertical(self):
        result = utils.connect_2d_shapes(self.shapes, 10, 'vertical')
        assert result == self.union

    def test_horizontal(self):
        result = utils.connect_2d_shapes(self.shapes, 10, 'horizontal')
        vector = [0, 1, 0]
        assert result == ast.Rotate(90, vector, self.union)


def test_connect_heterogenous_handling():
    """Assert that heterogenous shapes cannot be merged."""
    shapes = [ast.Circle(5), ast.Rectangle(2, 3)]
    with pytest.raises(NotImplementedError):
        utils.connect_2d_shapes(shapes, 10, 'vertical')


def test_connect_invalid_arguments():
    """Test that arguments for ``connect_2d_shapes`` are validated."""
    shapes = [ast.Circle(5), ast.Circle(2)]
    with pytest.raises(AssertionError):
        utils.connect_2d_shapes(shapes, 10, 'diagonal')
