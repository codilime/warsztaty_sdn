import unittest
import json
from unittest.mock import patch

from ..app import app, router


class TestRouterFlaskaap(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        rv = self.client.get('/hello')
        self.assertEqual(b'hello', rv.data)
        self.assertEqual(200, rv.status_code)

    @patch.object(router, 'add_network', return_value=None)
    def test_create_network(self, mock_add_net):
        data = {
            'name': 'ala'
        }
        rv = self.client.post('/create/network', data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(b'Success\n', rv.data)
        self.assertEqual(200, rv.status_code)

    @patch.object(router, 'add_logical_port', return_value=None)
    def test_create_logical_port(self, add_logical_port):
        data = {
            'name': 'ala',
            'ip': '192.168.0.1'
        }
        rv = self.client.post('/create/logical_port', data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(b'Success\n', rv.data)
        self.assertEqual(200, rv.status_code)

    @patch.object(router, 'remove_logical_port', return_value=None)
    def test_create_logical_port(self, remove_logical_port):
        data = {
            'name': 'ala',
            'ip': '192.168.0.1'
        }
        rv = self.client.delete('/logical_port', data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(b'Success\n', rv.data)
        self.assertEqual(200, rv.status_code)