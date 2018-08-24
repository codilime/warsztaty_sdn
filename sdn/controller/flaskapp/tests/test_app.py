import unittest
import json
from ..app import app, ServerError, _assert_proper_request, controller
from unittest.mock import patch, MagicMock

from sdn.controller.container import Container
from sdn.controller.router import Router
from docker.client import DockerClient


class Req(object):
    def __init__(self):
        self.content_type = 'application/json'
        self.json = {}


class TestControllerFlaskaap(unittest.TestCase):
    ROUTER_URL = "10.0.0.1"
    ROUTER_ID = "router-id"
    CONTAINER_RED_URL = "10.0.0.2"
    CONTAINER_RED_ID = "red-id"
    CONTAINER_GREEN_URL = "10.0.0.3"
    CONTAINER_GREEN_ID = "green-id"

    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        """Start with a blank database."""
        rv = self.client.get('/hello')
        self.assertEqual(b'hello', rv.data)
        self.assertEqual(200, rv.status_code)

    def test_assert_proper_request(self):
        req = Req()
        _assert_proper_request(req)

    def test_assert_proper_request_wrong_content_type(self):
        req = Req()
        req.content_type = 'wrong_content_type'
        with self.assertRaises(ServerError) as context:
            _assert_proper_request(req)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, 'Malformed request, expected json payload and type')
        self.assertIsNone(context.exception.payload)

    def test_assert_proper_request_without_json(self):
        req = Req()
        del req.json
        with self.assertRaises(ServerError) as context:
            _assert_proper_request(req)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, 'Malformed request, expected json payload and type')
        self.assertIsNone(context.exception.payload)

    def test_get_index(self):
        rv = self.client.get('/')
        self.assertTrue(b'Available endpoints:' in rv.data)
        self.assertEqual(200, rv.status_code)
        rv = self.client.get('/index')
        self.assertTrue(b'Available endpoints:' in rv.data)
        self.assertEqual(200, rv.status_code)

    def test_force_clean(self):
        rv = self.client.post('/force_clean')
        self.assertEqual(b'Success\n', rv.data)
        self.assertEqual(200, rv.status_code)

    def test_create_network(self):
        with patch.object(controller, 'add_network') as mock:
            data = {
                'id': 'ala',
                'ip': '192.168.0.0/24'
            }
            rv = self.client.post('/create/network', data=json.dumps(data),
                                  content_type='application/json')
            self.assertEqual(b'Success\n', rv.data)
            self.assertEqual(200, rv.status_code)

    def test_create_network_fail(self):
        with patch.object(controller, 'add_network') as mock:
            data = {
                'id': 'ala'
            }
            rv = self.client.post('/create/network', data=json.dumps(data),
                                  content_type='application/json')
            self.assertEqual(500, rv.status_code)
            data = json.loads(rv.data.decode('utf-8'))
            self.assertTrue('Internal server error when creating network' in data['message'])


    @patch.object(Router, 'add_network')
    @patch.object(Router, 'delete_network')
    def test_delete_network(self, router_add_mock, router_delete_mock):
        network_id = 'new-network'
        data = {
            'id': network_id,
            'ip': '1.1.1.1/32'
        }
        self.client.post('/create/network', data=json.dumps(data),
                         content_type='application/json')

        rv = self.client.delete('/network/{network_id}'.format(network_id=network_id),
                                content_type='application/json')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'Success\n', rv.data)


    def test_delete_network_should_fail(self):
        network_id = 'non-existing-network'
        rv = self.client.delete('/network/{network_id}'.format(network_id=network_id),
                                content_type='application/json')
        self.assertEqual(rv.status_code, 500)
        self.assertIn('Internal server error when deleting network', rv.data.decode('utf-8'))


    @patch.object(Router, 'add_network')
    def test_should_list_networks(self, router_mock):
        n1 = {
            'id': 'ala',
            'ip': '192.168.0.0/24'
        }
        self.client.post('/create/network', data=json.dumps(n1),
                            content_type='application/json')
        n2 = {
            'id': 'ola',
            'ip': '192.168.1.0/24'
        }
        self.client.post('/create/network', data=json.dumps(n2),
                            content_type='application/json')

        rv = self.client.get('/networks')
        self.assertEqual(200, rv.status_code)
        response = json.loads(rv.data.decode('utf-8'))
        self.assertIn(n1, response)
        self.assertIn(n2, response)

    @patch.object(Container, 'start')
    def test_start_container(self, mock):
        data = {
            'id': 'ala',
        }
        rv = self.client.post('/create/container', data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(b'Success\n', rv.data)
        self.assertEqual(200, rv.status_code)
        mock.assert_called()

    @patch.object(Container, 'start')
    def test_should_list_containers(self, mock):
        c1 = {
            'id': 'ala',
        }
        self.client.post('/create/container', data=json.dumps(c1),
                              content_type='application/json')
        c2 = {
            'id': 'ola',
        }
        self.client.post('/create/container', data=json.dumps(c2),
                              content_type='application/json')

        rv = self.client.get('/containers')

        self.assertEqual(200, rv.status_code)

        response = json.loads(rv.data.decode('utf-8'))
        self.assertIn(c1, response)
        self.assertIn(c2, response)

    @patch.object(Container, 'start')
    @patch.object(Container, 'stop')
    def test_stop_container(self, start_mock, stop_mock):
        container_id = 'ala'
        data = {
            'id': container_id,
        }
        self.client.post('/create/container', data=json.dumps(data),
                         content_type='application/json')

        rv = self.client.delete('/container/{container_id}'.format(container_id=container_id),
                                content_type='application/json')
        self.assertEqual(b'Success\n', rv.data)
        self.assertEqual(200, rv.status_code)
        stop_mock.assert_called()

    @patch.object(controller, 'add_logical_port')
    @patch.object(controller, 'get_network')
    @patch.object(controller, 'add_network')
    @patch.object(Container, 'start')
    def test_create_logical_port(self, mock, mock2, mock3, mock_start):
        data = {
            'id': 'kot',
        }
        self.client.post('/create/container', data=json.dumps(data),
                              content_type='application/json')

        data_net = {
            'id': 'ala',
            'ip': '192.168.0.0/24'
        }
        self.client.post('/create/network', data=json.dumps(data_net),
                              content_type='application/json')
        data = {
            'net_id': 'ala',
            'container':
                {'id': 'kot'}
        }
        rv = self.client.post('/create/logical_port', data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(b'Success\n', rv.data)
        self.assertEqual(200, rv.status_code)

    @patch.object(controller, 'add_logical_port')
    @patch.object(controller, 'get_network')
    @patch.object(controller, 'add_network')
    def test_create_logical_port_fail_without_container(self,  mock, mock2, mock3):
        with patch.object(controller, 'add_logical_port') as mock:
            data_net = {
                'id': 'ala',
                'ip': '192.168.0.0/24'
            }
            self.client.post('/create/network', data=json.dumps(data_net),
                                  content_type='application/json')
            data = {
                'net_id': 'ala',
                # container data is missing
            }
            rv = self.client.post('/create/logical_port', data=json.dumps(data),
                                  content_type='application/json')
            self.assertEqual(500, rv.status_code)
            data = json.loads(rv.data.decode('utf-8'))
            self.assertTrue('Internal server error when creating logical port' in data['message'])

    @patch.object(DockerClient, 'networks')
    @patch.object(Router, 'add_network')
    @patch.object(Router, 'add_logical_port')
    @patch.object(Container, 'start')
    @patch.object(Container, 'add_logical_port')
    def test_should_list_logical_ports(self, mock, mock2, mock3, mock4, mock5):
        data = {
            'id': 'kot',
        }
        self.client.post('/create/container', data=json.dumps(data),
                              content_type='application/json')

        data_net = {
            'id': 'ala',
            'ip': '192.168.0.0/24'
        }
        rv = self.client.post('/create/network', data=json.dumps(data_net),
                              content_type='application/json')
        self.assertEqual(200, rv.status_code)

        data_lp = {
            'id': 'kot-ala',
            'net_id': 'ala',
            'container':
                {'id': 'kot'}
        }
        rv = self.client.post('/create/logical_port', data=json.dumps(data_lp),
                              content_type='application/json')
        self.assertEqual(200, rv.status_code)

        rv = self.client.get('/logical_ports')

        self.assertEqual(200, rv.status_code)
        response = json.loads(rv.data.decode('utf-8'))
        self.assertEqual([data_lp], response)