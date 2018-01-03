#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pypeep.pypeep_resource.prepare import prepare, _SOURCE
import os
import tempfile
import pytest


def mock_python_path(lib_name, python_version):
    tmp_dir = tempfile.mkdtemp()
    lib_dir = os.path.join(tmp_dir, lib_name, python_version)
    os.makedirs(lib_dir)
    # Create empty files
    open(os.path.join(lib_dir, 'site.py'), 'a').close()
    if not os.path.exists(_SOURCE):
        os.makedirs(os.path.dirname(_SOURCE))
    open(_SOURCE, 'a').close()
    return tmp_dir


def test_hijack_export():
    pass


@pytest.mark.parametrize("lib_name,python_version", [
    ('lib', 'python2.7',),
    ('lib64', 'python2.7',),
    ('lib', 'python3.6',),
    ('lib64', 'python3.6',),
])
def test_prepare_script(lib_name, python_version):
    path = mock_python_path(lib_name, python_version)
    prepare(os.path.join(path, 'bin'), lib_name)
    assert os.path.exists(os.path.join(path, lib_name, python_version, 'sitecustomize.py'))
