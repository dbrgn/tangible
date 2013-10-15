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


def test_returncode():
    pyfiles = (f for f in os.listdir('examples') if f.endswith('.py'))
    for f in pyfiles:
        try:
            with chdir('examples'):
                subprocess.check_call('python ' + f, shell=True)
        except subprocess.CalledProcessError:
            pytest.fail('Example {} returned with status code != 0.'.format(f))
