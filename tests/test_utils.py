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


@pytest.mark.parametrize(('data', 'groups'), [
    ([1, 2, 3, 10, 11, 20, 28, 29], [6, 21, 77]),
    ([1], [1]),
    ([-1, -2, -3, 4, 5, 6], [-6, 15]),
])
def test_reduceby_sum(data, groups):
    keyfunc = lambda x: x // 10
    reducefunc = lambda x, y: x + y
    generator = utils.reduceby(data, keyfunc, reducefunc, 0)
    assert list(generator) == groups


@pytest.mark.parametrize(('data', 'groups'), [
    ([0, 2, 4, 6, 8, 10, 1, 3, 5, 7, 9], [0, 945]),
    ([1], [1]),
    ([1, 1, 1, 42], [1, 42]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
])
def test_reduceby_product(data, groups):
    keyfunc = lambda x: x % 2 == 0
    reducefunc = lambda x, y: x * y
    generator = utils.reduceby(data, keyfunc, reducefunc, 1)
    assert list(generator) == groups


@pytest.mark.parametrize(('quads', 'triangles'), [
    ([[0, 1, 2, 3]], [[0, 1, 2], [0, 2, 3]]),
    ([[1, 3, 5, 7], [6, 5, 4, 3]], [[1, 3, 5], [1, 5, 7], [6, 5, 4], [6, 4, 3]]),
])
def test_quads_to_triangles(quads, triangles):
    assert utils.quads_to_triangles(quads) == triangles


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
                ], quads=[
                    [0, 1, 2, 3], [4, 7, 6, 5],
                    [0, 4, 5, 1], [1, 5, 6, 2], [2, 6, 7, 3], [3, 7, 4, 0],
                ])
            ),
            ast.Translate(0, 0, 10,
                ast.Polyhedron(points=[
                    [5.0, 3.0, 0], [-5.0, 3.0, 0], [-5.0, -3.0, 0], [5.0, -3.0, 0],
                    [3.0, 11.0, 10], [-3.0, 11.0, 10], [-3.0, -11.0, 10], [3.0, -11.0, 10],
                ], quads=[
                    [0, 1, 2, 3], [4, 7, 6, 5],
                    [0, 4, 5, 1], [1, 5, 6, 2], [2, 6, 7, 3], [3, 7, 4, 0],
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


class TestPolygonConnect(object):

    @classmethod
    def setup_class(cls):
        cls.shapes = [
            ast.Polygon(points=[(3, 0), (3, 4), (-2, 3), (-3, 0), (0, -2), (3, 0)]),
            ast.Polygon(points=[(3, 0), (0, 2), (-3, 0), (-2, -3), (2, -3), (3, 0)]),
            ast.Polygon(points=[(3, 0), (3, 4), (-2, 3), (-3, 0), (0, -2), (3, 0)]),
        ]
        quads = [[1, 0, 5, 6], [2, 1, 6, 7], [3, 2, 7, 8], [4, 3, 8, 9], [0, 4, 9, 5]]
        triangles = [
            [0, 1, 2], [7, 6, 5],
            [0, 2, 3], [8, 7, 5],
            [0, 3, 4], [9, 8, 5],
        ]
        cls.union = ast.Union(items=[
            ast.Translate(0, 0, 0,
                ast.Polyhedron(points=[
                    [3, 0, 0], [3, 4, 0], [-2, 3, 0], [-3, 0, 0], [0, -2, 0],
                    [3, 0, 5], [0, 2, 5], [-3, 0, 5], [-2, -3, 5], [2, -3, 5],
                ], quads=quads, triangles=triangles)
            ),
            ast.Translate(0, 0, 5,
                ast.Polyhedron(points=[
                    [3, 0, 0], [0, 2, 0], [-3, 0, 0], [-2, -3, 0], [2, -3, 0],
                    [3, 0, 5], [3, 4, 5], [-2, 3, 5], [-3, 0, 5], [0, -2, 5],
                ], quads=quads, triangles=triangles)
            ),
        ])

    def test_vertical_points(self):
        result = utils.connect_2d_shapes(self.shapes, 5, 'vertical')
        assert result.items[0].item.points == self.union.items[0].item.points
        assert result.items[1].item.points == self.union.items[1].item.points

    def test_vertical_triangles(self):
        result = utils.connect_2d_shapes(self.shapes, 5, 'vertical')
        assert result.items[0].item.triangles == self.union.items[0].item.triangles
        assert result.items[1].item.triangles == self.union.items[1].item.triangles

    def test_vertical_quads(self):
        result = utils.connect_2d_shapes(self.shapes, 5, 'vertical')
        assert result.items[0].item.quads == self.union.items[0].item.quads
        assert result.items[1].item.quads == self.union.items[1].item.quads

    def test_vertical(self):
        result = utils.connect_2d_shapes(self.shapes, 5, 'vertical')
        assert result == self.union

    def test_horizontal(self):
        result = utils.connect_2d_shapes(self.shapes, 5, 'horizontal')
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


@pytest.mark.parametrize(('data', 'result'), [
    ([], [[]]),
    ([1, 2, 3], [[1, 2, 3]]),
    ([[1, 2, 3]], [[1, 2, 3]]),
    ([[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]),
])
def test_ensure_list_of_lists(data, result):
    assert utils.ensure_list_of_lists(data) == result
