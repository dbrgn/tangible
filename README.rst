Tangible
========

Tangible is a Python library to convert data into tangible 3D models.

It generates code for different backends like OpenSCAD.

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

This library is work in progress and currently in the planning phase.
