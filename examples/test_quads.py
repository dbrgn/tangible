# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from tangible.shapes.base import Shape
from tangible import ast
from tangible.backends.openscad import OpenScadBackend


class Quads(Shape):

    def _build_ast(self):
        points = [
            (0, 0, 0), (0, 5, 0), (5, 5, 0), (5, 0, 0),
            (0, 0, 10), (0, 8, 10), (8, 8, 10), (8, 0, 10),
        ]
        quads = [
            (0, 3, 2, 1),
            (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
            (4, 5, 6, 7),
        ]
        return ast.Polyhedron(points=points, quads=quads)


q = Quads([])
code = q.render(backend=OpenScadBackend)
print(code)
