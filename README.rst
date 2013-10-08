Tangible
========

**WARNING: Project is still under initial development. Git history may be
changed and force-pushed at any time.**

Tangible is a Python library to convert data into tangible 3D models.

It generates code for different backends like OpenSCAD or ImplicitSCAD.

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

Work in progress, everything is still *very* unstable and might not work at all.


Coding Guidelines
-----------------

`PEP8 <http://www.python.org/dev/peps/pep-0008/>`__ via `flake8
<https://pypi.python.org/pypi/flake8>`_ with max-line-width set to 99 and
E126-E128 ignored.

Docstrings: `Sphinx style <http://stackoverflow.com/q/4547849/284318>`__.


Testing
-------

Install ``requirements-dev.txt``, then run ``py.test`` in the main directory.
Violations of the coding guidelines above will be counted as test fails.


License
-------

LGPLv3 `http://www.gnu.org/licenses/lgpl.html
<http://www.gnu.org/licenses/lgpl.html>`_
