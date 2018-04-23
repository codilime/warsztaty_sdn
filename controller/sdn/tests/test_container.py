import unittest
from unittest.mock import MagicMock
from ..logical_port import LogicalPort
from ..container import Container
from ..network import Network


class ContainerTests(unittest.TestCase):
    CONTAINER_URL = "10.0.0.1:5000"
    CONTAINER_ID = "container1"

    def test_should_store_single_logical_port(self):
        c = Container(self.CONTAINER_ID, self.CONTAINER_URL, MagicMock())
        p = LogicalPort(c, Network("net1", "192.168.0.0/24"))

        c.add_logical_port(p)

        self.assertListEqual(c.logical_ports, [p])

    def test_should_post_logical_port(self):
        poster = MagicMock()
        c = Container(self.CONTAINER_ID, self.CONTAINER_URL, poster)
        p = LogicalPort(c, Network("net1", "192.168.0.0/24"))

        c.add_logical_port(p)

        poster.post.assert_called_with(self.CONTAINER_URL + "/logical_port", "net_ip=192.168.0.0%2F24")


if __name__ == '__main__':
    unittest.main()
