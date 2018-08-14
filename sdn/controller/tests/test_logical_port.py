import unittest
from unittest.mock import MagicMock
from ..logical_port import LogicalPort
from ..container import Container
from ..network import Network


class LogicalPortsTests(unittest.TestCase):
    def test_should_compare_by_container_and_net(self):
        container = Container("c1", '', MagicMock(), MagicMock())
        other_container = Container("c2", '', MagicMock(), MagicMock())
        net = Network("net1", "192.168.0.0/24")
        other_net = Network("net2", "192.168.0.0/24")

        same1 = LogicalPort(container, net)
        same2 = LogicalPort(container, net)
        different_container = LogicalPort(other_container, net)
        different_net = LogicalPort(container, other_net)
        completely_different = LogicalPort(other_container, other_net)

        self.assertEqual(same1, same2)
        self.assertNotEqual(same1, different_container)
        self.assertNotEqual(same1, different_net)
        self.assertNotEqual(same1, completely_different)


if __name__ == '__main__':
    unittest.main()
