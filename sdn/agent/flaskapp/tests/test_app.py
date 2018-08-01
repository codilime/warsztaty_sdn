import unittest
import json
from ..app import app


class TestAgentFlaskaap(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        rv = self.client.get('/hello')
        self.assertEqual(b'hello', rv.data)
        self.assertEqual(200, rv.status_code)

    def test_ping_target_8888(self):
        rv = self.client.get('/ping/8.8.8.8')
        self.assertEqual(b'1', rv.data)
        self.assertEqual(200, rv.status_code)

    def test_ping_target_12700257(self):
        rv = self.client.get('/ping/127.0.0.257')
        self.assertEqual(b'0', rv.data)
        self.assertEqual(200, rv.status_code)

    def test_create_logical_port(self):
        data = {
            'net': 'ala',
            'net_ip' : '192.168.0.0/24',
            'router_ip': '10.0.0.1',
            'local_ip': '192.168.0.11'
        }
        rv = self.client.post('/create/logical_port', data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(b'Success\n', rv.data)
        self.assertEqual(200, rv.status_code)

    def test_create_logical_port_without_data(self):
        data = {}
        rv = self.client.post('/create/logical_port', data=json.dumps(data),
                              content_type='application/json')
        print(rv.data)
        self.assertEqual(b'Failed, not enough data\n', rv.data)
        self.assertEqual(400, rv.status_code)
