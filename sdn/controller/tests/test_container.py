import json
import docker
import docker.errors
import unittest
from unittest.mock import MagicMock
from ..logical_port import LogicalPort
from ..container import Container
from ..network import Network


class ContainerTests(unittest.TestCase):
    CONTAINER_URL = "10.0.0.1"
    CONTAINER_ID = "container1"

    def setUp(self):
        self.containers = []
        self.docker_client = docker.from_env()

    def tearDown(self):
        for name in self.containers:
            try:
                c = self.docker_client.containers.get(name)
                c.remove(force=True)
            except docker.errors.NotFound:
                pass

    def register_cleanup(self, name):
        self.containers.append(name)

    def assertRunning(self, name):
        c = self.docker_client.containers.get(name)
        self.assertEqual(c.status, 'running')

    def assertNoContainer(self, name):
        with self.assertRaises(docker.errors.NotFound):
            self.docker_client.containers.get(name)

    def test_should_start_stop_container(self):
        self.register_cleanup(self.CONTAINER_ID)
        c = Container(self.CONTAINER_ID, self.CONTAINER_URL, MagicMock(), self.docker_client)

        c.start()
        self.assertRunning(self.CONTAINER_ID)

        c.stop()
        self.assertNoContainer(self.CONTAINER_ID)

    def test_should_store_single_logical_port(self):
        c = Container(self.CONTAINER_ID, self.CONTAINER_URL, MagicMock(), MagicMock())
        p = LogicalPort(c, Network("net1", "192.168.0.0/24"))
        p.container_ip = '192.168.0.2'
        p.router_ip = '192.168.0.1'
        p.underlay_network_ip = "192.168.0.0/24"

        c.add_logical_port(p)

        self.assertListEqual(c.logical_ports, [p])

    def test_should_post_logical_port(self):
        poster = MagicMock()
        c = Container(self.CONTAINER_ID, self.CONTAINER_URL, poster, MagicMock())
        p = LogicalPort(c, Network("net1", "192.168.0.0/24"))
        p.container_ip = '192.168.0.2'
        p.router_ip = '192.168.0.1'
        p.underlay_network_ip = "192.168.0.0/24"

        c.add_logical_port(p)

        poster.post.assert_called_with("http://"+self.CONTAINER_URL + ":8090/create/logical_port",
                                       data=json.dumps({"net_id": "net1", "net_ip": "192.168.0.0/24", "router_ip": "192.168.0.1", "ip": "192.168.0.2"}, sort_keys=True),
                                       headers={'content-type': 'application/json'})

if __name__ == '__main__':
    unittest.main()
