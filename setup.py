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
          'Development Status :: 1 - Planning',
      ],
    )
