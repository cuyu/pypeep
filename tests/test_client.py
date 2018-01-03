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


@pytest.fixture(scope="class")
def ssh_client():
    client = Client(host='localhost', ssh_username='root', ssh_password='root', ssh_port=2222)
    return client


@pytest.fixture(params=['docker_client', 'ssh_client'])
def client(request):
    return request.getfuncargvalue(request.param)


class TestDockerClient(object):
    def test_execute(self, client):
        _, result, _ = client.execute('pwd')
        assert result

    def test_send_file(self, client):
        _, path = tempfile.mkstemp(suffix='abcdefg')
        filename = os.path.basename(path)
        client.send_files(path, '/tmp/{0}'.format(filename))
        _, result, _ = client.execute('ls /tmp')
        for name in result.split('\n'):
            if name == filename:
                break
        else:
            assert False, 'File not found in container'

    def test_send_folder(self, client):
        # Create empty folder and sub folder/files in it
        path = tempfile.mkdtemp(suffix='qazxsw')
        os.makedirs(os.path.join(path, 'sub', 'sub'))
        open(os.path.join(path, 'sub', 'aaa'), 'a').close()

        filename = os.path.basename(path)
        client.send_files(path, '/tmp/{0}'.format(filename))
        _, result, _ = client.execute('ls /tmp')
        for name in result.split('\n'):
            if name == filename:
                break
        else:
            assert False, 'File not found in container'

    def test_fetch_file(self, client):
        filename = 'qwerasdf'
        client.execute('touch /tmp/{0}'.format(filename))
        local_path = '/tmp/{0}'.format(filename)
        remote_path = local_path
        client.fetch_files(remote_path, local_path)
        assert os.path.exists(local_path)

    def test_fetch_folder(self, client):
        filename = 'zxcvasdf'
        client.execute('mkdir /tmp/{0}'.format(filename))
        client.execute('touch /tmp/{0}/bbb'.format(filename))
        local_path = '/tmp/{0}'.format(filename)
        client.fetch_files('/tmp', local_path)
        assert os.path.exists(local_path)
