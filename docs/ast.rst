.. _ast:

AST
===

The abstract syntax tree provides different shape types and transformations that
can be nested. They're largely inspired by `OpenSCAD
<http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language>`_.


2D Shapes
---------

.. autoclass:: tangible.ast.Circle
    :members:

.. autoclass:: tangible.ast.CircleSector
    :members:

.. autoclass:: tangible.ast.Rectangle
    :members:

.. autoclass:: tangible.ast.Polygon
    :members:


3D Shapes
---------

.. autoclass:: tangible.ast.Cube
    :members:

.. autoclass:: tangible.ast.Sphere
    :members:

.. autoclass:: tangible.ast.Cylinder
    :members:

.. autoclass:: tangible.ast.Polyhedron
    :members:


Transformations
---------------

.. autoclass:: tangible.ast.Translate
    :members:

.. autoclass:: tangible.ast.Rotate
    :members:

.. autoclass:: tangible.ast.Scale
    :members:

.. autoclass:: tangible.ast.Mirror
    :members:


Boolean operations
------------------

.. autoclass:: tangible.ast.Union
    :members:

.. autoclass:: tangible.ast.Difference
    :members:

.. autoclass:: tangible.ast.Intersection
    :members:


Extrusions
----------

.. autoclass:: tangible.ast.LinearExtrusion
    :members:

.. autoclass:: tangible.ast.RotateExtrusion
    :members:
