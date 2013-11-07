# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from tangible import shapes
from tangible.shapes import Shape


data1d_flat = [1, 2, 3, 4, 5]
data1d_nested = [[1, 2, 3, 4, 5]]
data2d = [[1, 2, 3], [4, 5, 6]]
data4d = [[1, 2], [3, 4], [5, 6], [7, 8]]


@pytest.mark.parametrize('data', [
    [1, 2, 3],
    (1, 2, 3),
    [[1, 2], [3, 4, 5], (6, 7)],
])
def test_valid_base_shape(data):
    try:
        Shape(data)
    except ValueError:
        pytest.fail()


@pytest.mark.parametrize('data', [
    '',
    None,
])
def test_invalid_base_shape(data):
    with pytest.raises(ValueError):
        Shape(data)


@pytest.mark.parametrize(('data', 'Mixin'), [
    ([], shapes.Data1DMixin),
    (data1d_flat, shapes.Data2DMixin),
    (data1d_nested, shapes.Data2DMixin),
    (data4d, shapes.Data2DMixin),
    (data1d_flat, shapes.Data4DMixin),
    (data1d_nested, shapes.Data4DMixin),
    (data2d, shapes.Data4DMixin),
])
def test_dimension_mixin_fails(data, Mixin):
    class MyShape(Mixin, Shape):
        pass
    with pytest.raises(ValueError):
        MyShape(data)


@pytest.mark.parametrize(('data', 'Mixin'), [
    (data1d_flat, shapes.Data1DMixin),
    (data1d_nested, shapes.Data1DMixin),
    (data2d, shapes.Data2DMixin),
    (data4d, shapes.Data4DMixin),
])
def test_dimension_mixin_success(data, Mixin):
    class MyShape(Mixin, Shape):
        pass
    try:
        MyShape(data)
    except:
        pytest.fail()


@pytest.mark.parametrize('data', [
    [],
    [1],
    [[1]],
    [[1], [2, 3]],
    [[1, 2], [3, 4, 5], [6, 7]],
    [xrange(200), xrange(200), xrange(201)],
])
def test_same_length_dataset_mixin_fails(data):
    class MyShape(shapes.SameLengthDatasetMixin, Shape):
        pass
    with pytest.raises(ValueError):
        MyShape(data)


@pytest.mark.parametrize('data', [
    [[1], [2]],
    [[1, 2], [2, 3]],
    [xrange(200), xrange(200), xrange(200)],
])
def test_same_length_dataset_mixin_success(data):
    class MyShape(shapes.SameLengthDatasetMixin, Shape):
        pass
    try:
        MyShape(data)
    except:
        pytest.fail()
