Welcome to Tangible's documentation!
====================================

.. image:: https://travis-ci.org/dbrgn/tangible.png
    :target: https://travis-ci.org/dbrgn/tangible
    :alt: Build Status

Tangible is a Python library to convert data into tangible 3D models. It
generates code for different backends like OpenSCAD or ImplicitSCAD. It is
inspired by projects like OpenSCAD and d3.js.

The difference from Projects like SolidPython is that Tangible is a modular
system with an intermediate representation of objects that is capable of
generating code for different backends, not just OpenSCAD. Additionally, its
main focus is not general CAD, but printable 3D visualization of data.

.. image:: https://raw.github.com/dbrgn/tangible/master/example1.jpg
    :alt: Example 1

The workflow is as follows::

    Python code => Intermediate representation (AST) => Programmatic CAD code
    => STL file => Slicer => G code => 3D printer => Tangible object

Source code: `https://github.com/dbrgn/tangible
<https://github.com/dbrgn/tangible>`_

Contributions are very welcome! Please open an issue or a pull request `on
Github <https://github.com/dbrgn/tangible>`_.


Table of Contents
=================

**Using the library**

.. toctree::
    :maxdepth: 2

    installing
    usage
    examples

**Reference**

.. toctree::
    :maxdepth: 2

    shapes
    scales
    utils
    ast
    backends


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
