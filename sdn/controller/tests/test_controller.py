import unittest
import docker.types
from unittest.mock import MagicMock
from ..logical_port import LogicalPort
from ..container import Container
from ..router import Router
from ..controller import Controller
from ..network import Network


class ControllerTest(unittest.TestCase):
    ROUTER_URL = "10.0.0.1"
    ROUTER_ID = "router-id"
    CONTAINER_RED_URL = "10.0.0.2"
    CONTAINER_RED_ID = "red-id"
    CONTAINER_GREEN_URL = "10.0.0.3"
    CONTAINER_GREEN_ID = "green-id"

    def test_should_post_network_to_router(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)
        ctrl = Controller(r, MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        poster.post.assert_called_with(
            self.ROUTER_URL + "/create/network",
            data='{"id": "net1"}',
            headers={'content-type': 'application/json'}
        )

    def test_should_lookup_networks_by_id(self):
        ctrl = Controller(MagicMock(), MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        stored_net = ctrl.get_network("net1")
        self.assertEqual(n, stored_net)

    def test_should_post_logical_port_to_router(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)
        c = Container(self.CONTAINER_RED_ID, self.CONTAINER_RED_URL, MagicMock())
        ctrl = Controller(r, MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        p = LogicalPort(c, n)
        ctrl.add_logical_port(p)

        poster.post.assert_called_with(
            self.ROUTER_URL + "/create/logical_port",
            data='{"net_id": "net1", "ip": "192.168.0.2"}',
            headers={'content-type': 'application/json'}
        )

    def test_should_post_logical_port_to_container(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, MagicMock())
        c = Container(self.CONTAINER_RED_ID, self.CONTAINER_RED_URL, poster)
        ctrl = Controller(r, MagicMock())

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        p = LogicalPort(c, n)
        ctrl.add_logical_port(p)

        poster.post.assert_called_with("http://"+self.CONTAINER_RED_URL + ":8090/create/logical_port",
                                       data='{"net_id": "net1", "net_ip": "192.168.0.0/24", "router_ip": "192.168.0.2", "ip": "192.168.0.3"}',
                                       headers={'content-type': 'application/json'})

    def test_should_attach_logical_port_to_network(self):
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)
        c = Container(self.CONTAINER_RED_ID, self.CONTAINER_RED_URL, MagicMock())
        docker_client = MagicMock()
        ctrl = Controller(r, docker_client)

        n = Network("net1", "192.168.0.0/24")
        ctrl.add_network(n)

        p = LogicalPort(c, n)
        mocked_network = MagicMock()
        docker_client.networks.create = MagicMock(return_value=mocked_network)
        ctrl.add_logical_port(p)

        poster.post.assert_called_with(
            self.ROUTER_URL + "/create/logical_port",
            data='{"net_id": "net1", "ip": "192.168.0.2"}',
            headers={'content-type': 'application/json'}
        )
        mocked_network.connect.assert_any_call(self.ROUTER_ID, ipv4_address='192.168.0.2')
        mocked_network.connect.assert_any_call(self.CONTAINER_RED_ID, ipv4_address='192.168.0.3')


if __name__ == '__main__':
    unittest.main()
