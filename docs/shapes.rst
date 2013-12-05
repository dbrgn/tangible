Shapes
======

Shapes make it easier to generate specific models from data, without having to
manipulate AST objects directly.

Shape Types
-----------

All shapes are grouped into categories. Click on one of the categories to see a
detailed list of shapes.

.. toctree::
    :maxdepth: 1

    shapes/bars
    shapes/vertical
    shapes/pie

Base Classes
------------

.. inheritance-diagram::
    tangible.shapes.base.Shape
    tangible.shapes.bars.BarsShape
    tangible.shapes.vertical.VerticalShape
    tangible.shapes.pie.PieShape
    :parts: 2

.. autoclass:: tangible.shapes.base.Shape
    :members:

.. autoclass:: tangible.shapes.bars.BarsShape
    :members:
    :noindex:

.. autoclass:: tangible.shapes.vertical.VerticalShape
    :members:
    :noindex:

.. autoclass:: tangible.shapes.pie.PieShape
    :members:
    :noindex:


Inheritance Diagram
-------------------

.. inheritance-diagram::
    tangible.shapes.base
    tangible.shapes.bars
    tangible.shapes.vertical
    tangible.shapes.pie
    :parts: 2
