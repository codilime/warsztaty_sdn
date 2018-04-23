import unittest
from unittest.mock import MagicMock
from ..router import Router
from ..network import Network
from ..logical_port import LogicalPort


class RouterTests(unittest.TestCase):
    ROUTER_URL = "10.0.0.1:5000"
    ROUTER_ID = "router-id"

    def test_should_store_single_network(self):
        n = Network("net1", "192.168.0.0/24")
        r = Router(self.ROUTER_ID, self.ROUTER_URL, MagicMock())

        r.add_network(n)

        self.assertListEqual(r.networks, [n])

    def test_should_store_multiple_networks(self):
        n1 = Network("net1", "192.168.0.0/24")
        n2 = Network("net2", "192.168.1.0/24")
        r = Router(self.ROUTER_ID, self.ROUTER_URL, MagicMock())

        r.add_network(n1)
        r.add_network(n2)

        self.assertListEqual(r.networks, [n1, n2])

    def test_should_post_network(self):
        n = Network("net1", "192.168.0.0/24")
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)

        r.add_network(n)

        poster.post.assert_called_with(self.ROUTER_URL+"/network", "id=net1")

    def test_should_store_single_logical_port(self):
        p = LogicalPort(None, Network('net1', '192.168.0.0/24'))
        p.router_ip = "192.168.0.1"
        r = Router(self.ROUTER_ID, self.ROUTER_URL, MagicMock())

        r.add_logical_port(p)

        self.assertListEqual(r.logical_ports, [p])

    def test_should_post_logical_port(self):
        p = LogicalPort(None, Network('net1', '192.168.0.0/24'))
        p.router_ip = "192.168.0.1"
        poster = MagicMock()
        r = Router(self.ROUTER_ID, self.ROUTER_URL, poster)

        r.add_logical_port(p)

        poster.post.assert_called_with(self.ROUTER_URL + "/logical_port", "net_id=net1&ip=192.168.0.1")


if __name__ == '__main__':
    unittest.main()
