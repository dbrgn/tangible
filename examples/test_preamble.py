# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible.shapes.base import Shape
from tangible import ast
from tangible.backends.openscad import OpenScadBackend


class Circle(Shape):
    def _build_ast(self):
        return ast.Difference([
            ast.CircleSector(10, 270),
            ast.CircleSector(10, 45),
        ])


q = Circle([])
code = q.render(backend=OpenScadBackend)
print(code)
