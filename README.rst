Tangible
========

.. image:: https://secure.travis-ci.org/dbrgn/tangible.png?branch=master
    :alt: Travis-CI build status
    :target: http://travis-ci.org/dbrgn/tangible

.. image:: https://coveralls.io/repos/dbrgn/tangible/badge.png?branch=master
    :target: https://coveralls.io/r/dbrgn/tangible
    :alt: Coverage Status

**WARNING: Project is still under initial development. Git history may be
changed and force-pushed at any time.**

*Tangible* is a Python library to convert data into tangible 3D models. It
generates code for different backends like *OpenSCAD* or *ImplicitSCAD*. It is
inspired by projects like *OpenSCAD* and *d3.js*.

.. image:: https://raw.github.com/dbrgn/tangible/master/example1.jpg
    :alt: Example 1

The difference from Projects like *SolidPython* is that *Tangible* is a modular
system with an intermediate representation of objects that is capable of
generating code for different backends, not just *OpenSCAD*. Additionally, its
main focus is not general CAD, but printable 3D visualization of data.

The workflow to get a real object from data is as follows::

    Python code => Intermediate representation (AST) => Programmatic CAD code
    => STL file => Slicer => G code => 3D printer => Tangible object

Of these, *Tangible* does the first three steps. The fourth step is handled by
a programmatic CAD tool like *OpenSCAD* or *ImplicitSCAD* and the last four
steps are handled by the specific 3D printer software.

This library is my student research project thesis at `HSR <http://hsr.ch/>`_.
Work is still in progress, everything is still *very* unstable.

Currently supported Python versions are 2.7. Support for 2.6 and 3.3+ is
planned.


Documentation
-------------

Documentation can be found on ReadTheDocs: `http://tangible.readthedocs.org/
<http://tangible.readthedocs.org/>`_


Coding Guidelines
-----------------

`PEP8 <http://www.python.org/dev/peps/pep-0008/>`__ via `flake8
<https://pypi.python.org/pypi/flake8>`_ with max-line-width set to 99 and
E126-E128 ignored.

All Python files must start with an UTF8 encoding declaration and some
`future-imports <http://stackful-dev.com/quick-tips-on-making-your-code-python-3-ready.html>`_:

.. sourcecode:: python

    # -*- coding: utf-8 -*-
    from __future__ import print_function, division, absolute_import, unicode_literals

Docstrings convention: `Sphinx style <http://stackoverflow.com/q/4547849/284318>`__.


Testing
-------

Install ``requirements-dev.txt``, then run ``py.test`` in the main directory.
Violations of the PEP8 coding guidelines above will be counted as test fails.


License
-------

LGPLv3 `http://www.gnu.org/licenses/lgpl.html
<http://www.gnu.org/licenses/lgpl.html>`_
