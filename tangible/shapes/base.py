# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals


class Shape(object):
    """The base class for all shapes.

    This class provides the base functionality to store data, build an `AST
    <ast.html>`_ and render it using the selected `backend <backends.html>`_.

    """
    def __init__(self, data):
        """
        :param data: The data.
        :type data: sequence type
        """
        self.data = data
        if not hasattr(data, '__iter__'):
            raise ValueError('Data must be a sequence type (e.g. a list)')

    def _build_ast(self):
        raise NotImplementedError('_build_ast method not implemented.')

    def render(self, backend):
        """Build the AST_ and generate code using the selected backend_.

        :param backend: The backend_ class used to process the AST_. Must accept
            the AST as constructor argument and provide a ``generate()`` method.
        :returns: The resulting source code as a string.

        """
        self.ast = self._build_ast()
        return backend(self.ast).generate()
