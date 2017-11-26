# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import subprocess
from contextlib import contextmanager

import pytest


@contextmanager
def chdir(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)


@pytest.mark.parametrize('pyfile', [f for f in os.listdir('examples') if f.endswith('.py')])
def test_returncode(pyfile):
    try:
        with chdir('examples'):
            subprocess.check_call('python ' + pyfile, shell=True)
    except subprocess.CalledProcessError:
        pytest.fail('Example {} returned with status code != 0.'.format(pyfile))
