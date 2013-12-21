#!/usr/bin/env python

from setuptools import setup
import tangible

readme = open('README.rst').read()

setup(name='tangible',
      version=tangible.__VERSION__,
      description='A Python library to convert data into tangible 3D models.',
      long_description=readme,
      author=tangible.__AUTHOR__,
      author_email=tangible.__AUTHOR_EMAIL__,
      url='https://github.com/dbrgn/tangible',
      license='LGPLv3',
      keywords='tangible visualization 3d printing',
      packages=['tangible'],
      platforms=['any'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 2 :: Only',
          'Topic :: Artistic Software',
          'Topic :: Multimedia :: Graphics :: 3D Modeling',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
    )
