# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from .. import utils


class BaseShape(object):
    """The base shape.

    In contrast to the :class:`Shape` class, it works without data. It provides
    a ``render`` method and an unimplemented ``_build_ast`` stub.

    """
    def _build_ast(self):
        raise NotImplementedError('_build_ast method not implemented.')

    def render(self, backend):
        """Build the AST_ and generate code using the selected backend_.

        :param backend: The backend_ class used to process the AST_. Must accept
            the AST as constructor argument and provide a ``generate()`` method.
        :returns: The resulting source code as a string.

        """
        ast = self._build_ast()
        return backend(ast).generate()


class Shape(BaseShape):
    """The base class for all shapes.

    This class provides the base functionality to store data, build an `AST
    <ast.html>`_ and render it using the selected `backend <backends.html>`_.

    """
    def __init__(self, data):
        """
        :param data: The data.
        :type data: sequence type
        :raises: ValueError if data is empty.
        """
        self.data = utils._ensure_list_of_lists(data)
        if len(self.data[0]) == 0:
            raise ValueError('Data may not be empty.')
