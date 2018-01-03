#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import os
import xml.etree.ElementTree as et
from pypeep.main import config_IDE


@pytest.mark.parametrize('server_name,remote_path,project_name,local_path,local_ip,local_port,ssh_port', [
    ('server0', '/dev/test0', 'test0', '/tmp/test0', '10.66.6.6', '32045', '2222'),
])
def test_workspace_configuration(server_name, remote_path, project_name, local_path, local_ip, local_port, ssh_port):
    if not os.path.isdir(local_path):
        os.makedirs(local_path)
    config_IDE(server_name, remote_path, project_name, local_path, local_ip, local_port, ssh_port)
    assert os.path.exists(os.path.join(local_path, '.idea'))
    assert os.path.exists(os.path.join(local_path, '.idea', 'workspace.xml'))
    workspace = et.parse(os.path.join(local_path, '.idea', 'workspace.xml'))
    assert workspace.findall(".//*[@name='PORT']")[0].attrib['value'] == local_port
    assert workspace.findall(".//*[@name='HOST']")[0].attrib['value'] == local_ip
    remote_mappings = et.parse(os.path.join(local_path, '.idea', 'remote-mappings.xml'))
    assert remote_mappings.findall(".//mapping")[0].attrib['remote-root'] == remote_path
