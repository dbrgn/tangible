# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from contextlib import contextmanager

from tangible import ast


class Statement(object):

    def __init__(self, text, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', ';')
        if kwargs:
            raise TypeError('invalid keyword arguments %r' % (kwargs.keys(),))
        if args:
            text = text.format(*args)
        self.text = text

    def render(self):
        return [self.text + self.suffix]


EmptyStatement = Statement('', suffix='')


class Block(object):

    def __init__(self, text, *args, **kwargs):
        self.prefix = kwargs.pop('prefix', '{')
        self.suffix = kwargs.pop('suffix', '};')
        if kwargs:
            raise TypeError('invalid keyword arguments %r' % (kwargs.keys(),))
        self.title = Statement(text, *args, suffix='')
        self.children = []
        self.stack = []

    def _get_head(self):
        if not self.stack:
            return self
        else:
            return self.stack[-1]

    def emptyline(self, count=1):
        for i in xrange(count):
            self._get_head().children.append(EmptyStatement)

    def statement(self, *args, **kwargs):
        self._get_head().children.append(Statement(*args, **kwargs))

    @contextmanager
    def block(self, *args, **kwargs):
        blk = Block(*args, **kwargs)
        self._get_head().children.append(blk)
        self.stack.append(blk)
        yield blk
        self.stack.pop(-1)

    def render(self):
        lines = self.title.render()
        if self.prefix:
            lines.append(self.prefix)
        for child in self.children:
            lines.extend(' ' * 4 + l for l in child.render())
        if self.suffix:
            lines.append(self.suffix)
        return lines


class Program(Block):

    def __init__(self):
        super(Program, self).__init__(None)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def render(self):
        lines = []
        for child in self.children:
            lines.extend(child.render())
        return '\n'.join(lines)


class OpenScadBackend(object):
    """Render AST to OpenSCAD source code."""

    def __init__(self, ast):
        """
        :param ast: The AST that should be rendered.
        :type ast: :class:`tangible.ast.AST` subclass

        """
        self.ast = ast

    def generate(self):
        """Generate OpenSCAD source code from the AST."""
        prgm = Program()
        BLOCK = prgm.block
        STMT = prgm.statement
        SEP = prgm.emptyline

        def _generate(node):
            """Recursive code generating function."""

            istype = lambda t: isinstance(node, t)

            # Handle lists

            if istype(list):
                for item in node:
                    _generate(item)

            # 2D shapes

            elif istype(ast.Circle):
                STMT('circle({})', node.radius)
            elif istype(ast.Rectangle):
                STMT('square([{}, {}]])', node.width, node.height)
            elif istype(ast.Polygon):
                points = map(list, node.points)
                paths = map(list, node.paths)
                if paths:
                    template = 'polygon(\npoints={!r},\n    paths={!r}\n)'
                    STMT(template, points, paths)
                else:
                    STMT('polygon(points={!r})', points)

            # 3D shapes

            elif istype(ast.Cube):
                STMT('cube([{}, {}, {}])', node.width, node.depth, node.height)
            elif istype(ast.Sphere):
                STMT('sphere(r={})', node.radius)
            elif istype(ast.Cylinder):
                STMT('cylinder({}, {}, {})', node.height, node.radius1, node.radius2)
            elif istype(ast.Polyhedron):
                points = map(list, node.points)
                if node.polygon_type == 'triangles':
                    # Triangles can be used directly
                    triangles = map(list, node.triangles)
                else:
                    # Quads have to be converted into triangles
                    triangles = []
                    for quad in node.quads:
                        triangles.append([quad[0], quad[1], quad[2]])
                        triangles.append([quad[0], quad[2], quad[3]])
                template = 'polyhedron(\npoints={!r},\n    triangles={!r}\n)'
                STMT(template, points, triangles)

            # Transformations

            elif istype(ast.Translate):
                with BLOCK('translate([{}, {}, {}])', node.x, node.y, node.z):
                    _generate(node.item)
            elif istype(ast.Rotate):
                with BLOCK('rotate({}, {!r})', node.degrees, node.vector):
                    _generate(node.item)
            elif istype(ast.Scale):
                with BLOCK('scale([{}, {}, {}])', node.x, node.y, node.z):
                    _generate(node.item)
            elif istype(ast.Mirror):
                with BLOCK('mirror([{}, {}, {}])', node.x, node.y, node.z):
                    _generate(node.item)

            # Boolean operations

            elif istype(ast.Union):
                with BLOCK('union()'):
                    _generate(node.items)
            elif istype(ast.Difference):
                with BLOCK('difference()'):
                    _generate(node.items)
            elif istype(ast.Intersection):
                with BLOCK('intersection()'):
                    _generate(node.items)

            # Extrusions

            elif istype(ast.LinearExtrusion):
                STMT('linear_extrude(height={})', node.height)
            elif istype(ast.RotateExtrusion):
                STMT('rotate_extrude(twist={})', node.twist)

        _generate(self.ast)

        return prgm.render()
