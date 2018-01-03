#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import os
import tempfile
from pypeep.client import Client


@pytest.fixture(scope="class")
def docker_client():
    host = os.environ['CONTAINER_ID']
    client = Client(host)
    return client


class TestDockerClient(object):
    def test_execute(self, docker_client):
        _, result, _ = docker_client.execute('pwd')
        assert result

    def test_send_file(self, docker_client):
        _, path = tempfile.mkstemp(suffix='abcdefg')
        filename = os.path.basename(path)
        docker_client.send_files(path, '/tmp/{0}'.format(filename))
        _, result, _ = docker_client.execute('ls /tmp')
        for name in result.split('\n'):
            if name == filename:
                break
        else:
            assert False, 'File not found in container'

    def test_send_folder(self, docker_client):
        path = tempfile.mkdtemp(suffix='qazxsw')
        filename = os.path.basename(path)
        docker_client.send_files(path, '/tmp/{0}'.format(filename))
        _, result, _ = docker_client.execute('ls /tmp')
        for name in result.split('\n'):
            if name == filename:
                break
        else:
            assert False, 'File not found in container'

    def test_fetch_file(self, docker_client):
        filename = 'qwerasdf'
        docker_client.execute('touch /tmp/{0}'.format(filename))
        local_path = '/tmp/{0}'.format(filename)
        remote_path = local_path
        docker_client.fetch_files(remote_path, local_path)
        assert os.path.exists(local_path)

    def test_fetch_folder(self, docker_client):
        filename = 'zxcvasdf'
        docker_client.execute('mkdir /tmp/{0}'.format(filename))
        local_path = '/tmp/{0}'.format(filename)
        remote_path = local_path
        docker_client.fetch_files(remote_path, local_path)
        assert os.path.exists(local_path)
