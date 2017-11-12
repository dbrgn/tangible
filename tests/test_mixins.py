# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from tangible.shapes import mixins
from tangible.shapes.base import Shape


data1d_flat = [1, 2, 3, 4, 5]
data1d_nested = [[1, 2, 3, 4, 5]]
data2d = [[1, 2, 3], [4, 5, 6]]
data4d = [[1, 2], [3, 4], [5, 6], [7, 8]]


@pytest.mark.parametrize(('data', 'Mixin'), [
    (data1d_flat, mixins.Data2DMixin),
    (data1d_nested, mixins.Data2DMixin),
    (data4d, mixins.Data2DMixin),
    (data1d_flat, mixins.Data4DMixin),
    (data1d_nested, mixins.Data4DMixin),
    (data2d, mixins.Data4DMixin),
])
def test_dimension_mixin_fails(data, Mixin):
    class MyShape(Mixin, Shape):
        pass
    with pytest.raises(ValueError):
        MyShape(data)


@pytest.mark.parametrize(('data', 'Mixin'), [
    (data1d_flat, mixins.Data1DMixin),
    (data1d_nested, mixins.Data1DMixin),
    (data2d, mixins.Data2DMixin),
    (data4d, mixins.Data4DMixin),
])
def test_dimension_mixin_success(data, Mixin):
    class MyShape(Mixin, Shape):
        pass
    try:
        MyShape(data)
    except:
        pytest.fail()


@pytest.mark.parametrize('data', [
    [[1], [2, 3]],
    [[1, 2], [3, 4, 5], [6, 7]],
    [range(200), range(200), range(201)],
])
def test_same_length_dataset_mixin_fails(data):
    class MyShape(mixins.SameLengthDatasetMixin, Shape):
        pass
    with pytest.raises(ValueError):
        MyShape(data)


@pytest.mark.parametrize('data', [
    [[1], [2]],
    [[1, 2], [2, 3]],
    [range(200), range(200), range(200)],
])
def test_same_length_dataset_mixin_success(data):
    class MyShape(mixins.SameLengthDatasetMixin, Shape):
        pass
    try:
        MyShape(data)
    except:
        pytest.fail()
