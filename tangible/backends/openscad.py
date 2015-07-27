# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from contextlib import contextmanager

from tangible import ast, utils


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
        self._preamble = set()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def preamble(self, item):
        self._preamble.add(item)

    def render(self):
        lines = list(self._preamble)
        if self._preamble:
            lines.append('')
        for child in self.children:
            lines.extend(child.render())
        return '\n'.join(lines)


class OpenScadBackend(object):
    """Render AST to OpenSCAD source code."""

    def __init__(self, ast):
        """
        :param ast: The AST that should be rendered.
        :type ast: Any :class:`tangible.ast.AST` subclass

        """
        self.ast = ast

    def generate(self):
        """Generate OpenSCAD source code from the AST."""
        prgm = Program()
        BLOCK = prgm.block
        STMT = prgm.statement
        PRE = prgm.preamble
        SEP = prgm.emptyline

        def _generate(node):
            """Recursive code generating function."""

            istype = lambda t: node.__class__ is t

            # Handle lists

            if istype(list):
                for item in node:
                    _generate(item)

            # 2D shapes

            elif istype(ast.Circle):
                STMT('circle({0})', node.radius)
            elif istype(ast.Rectangle):
                STMT('square([{0}, {1}])', node.width, node.height)
            elif istype(ast.Polygon):
                points = map(list, node.points)
                STMT('polygon({0!r})', points[:-1])
            elif istype(ast.CircleSector):
                PRE('module circle_sector(r, a) {\n'
                    '    a1 = a % 360;\n'
                    '    a2 = 360 - (a % 360);\n'
                    '    if (a1 <= 180) {\n'
                    '        intersection() {\n'
                    '            circle(r);\n'
                    '            polygon([\n'
                    '                [0,0],\n'
                    '                [0,r],\n'
                    '                [sin(a1/2)*r, r + cos(a1/2)*r],\n'
                    '                [sin(a1)*r + sin(a1/2)*r, cos(a1)*r + cos(a1/2)*r],\n'
                    '                [sin(a1)*r, cos(a1)*r],\n'
                    '            ]);\n'
                    '        }\n'
                    '    } else {\n'
                    '        difference() {\n'
                    '            circle(r);\n'
                    '            mirror([1,0]) {\n'
                    '                polygon([\n'
                    '                    [0,0],\n'
                    '                    [0,r],\n'
                    '                    [sin(a2/2)*r, r + cos(a2/2)*r],\n'
                    '                    [sin(a2)*r + sin(a2/2)*r, cos(a2)*r + cos(a2/2)*r],\n'
                    '                    [sin(a2)*r, cos(a2)*r],\n'
                    '                ]);\n'
                    '            };\n'
                    '        }\n'
                    '    }\n'
                    '};')
                STMT('circle_sector({0}, {1})', node.radius, node.angle)

            # 3D shapes

            elif istype(ast.Cube):
                STMT('cube([{0}, {1}, {2}])', node.width, node.depth, node.height)
            elif istype(ast.Sphere):
                STMT('sphere({0})', node.radius)
            elif istype(ast.Cylinder):
                STMT('cylinder({0}, {1}, {2})', node.height, node.radius1, node.radius2)
            elif istype(ast.Polyhedron):
                points = map(list, node.points)
                triangles = map(list, node.triangles) if node.triangles else []
                if node.quads:
                    triangles.extend(utils._quads_to_triangles(node.quads))
                template = 'polyhedron(\npoints={0!r},\n    triangles={1!r}\n)'
                STMT(template, points, triangles)

            # Transformations

            elif istype(ast.Translate):
                with BLOCK('translate([{0}, {1}, {2}])', node.x, node.y, node.z):
                    _generate(node.item)
            elif istype(ast.Rotate):
                with BLOCK('rotate({0}, {1!r})', node.degrees, list(node.vector)):
                    _generate(node.item)
            elif istype(ast.Scale):
                with BLOCK('scale([{0}, {1}, {2}])', node.x, node.y, node.z):
                    _generate(node.item)
            elif istype(ast.Mirror):
                with BLOCK('mirror({0!r})', list(node.vector)):
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
                with BLOCK('linear_extrude({0}, twist={1})', node.height, node.twist):
                    _generate(node.item)
            elif istype(ast.RotateExtrusion):
                with BLOCK('rotate_extrude()'):
                    _generate(node.item)

        _generate(self.ast)

        return prgm.render()
