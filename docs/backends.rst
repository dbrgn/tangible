Backends
========

OpenSCAD Backend
----------------

This backend allows generating of OpenSCAD code. To convert the code into an
STL file, you can either copy-and-paste the code into the GUI tool, or you can
render it directly using the ``openscad`` command line tool:

.. sourcecode:: bash

    python exampleModel.py > exampleModel.scad
    openscad -o exampleModel.stl --render exampleModel.scad

.. autoclass:: tangible.backends.openscad.OpenScadBackend
    :members:
