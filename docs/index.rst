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

The workflow is as follows::

    Tangible Python code
    ⇓
    Intermediate representation
    ⇓
    Programmatic CAD (OpenSCAD / ImplicitSCAD / ...)
    ⇓
    STL file
    ⇓
    Slicer
    ⇓
    G code
    ⇓
    Printed object


.. toctree::
   :maxdepth: 2

   shapes
   scales
   utils
   backends
   examples



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
