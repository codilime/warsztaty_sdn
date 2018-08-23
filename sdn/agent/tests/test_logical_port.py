import unittest
from ..logical_port import LogicalPort


class MockCmdExecutor(object):
    def __init__(self):
        self.commands = []

    def execute(self, cmd):
        self.commands.append(cmd)


class LogicalPortTest(unittest.TestCase):
    def test_should_add_default_route(self):
        mock_cmd = MockCmdExecutor()
        p = LogicalPort("net1", "192.168.0.0/24", "192.168.0.1", "192.168.0.2")

        p.create(mock_cmd)

        self.assertListEqual(mock_cmd.commands[0], ["ip", "route", "add", "192.168.0.0/24", "via", "192.168.0.1"])

    def test_should_remove_default_route(self):
        mock_cmd = MockCmdExecutor()
        p = LogicalPort("net1", "192.168.0.0/24", "192.168.0.1", "192.168.0.2")

        p.create(mock_cmd)
        p.delete(mock_cmd)

        self.assertListEqual(mock_cmd.commands[1], ["ip", "route", "del", "192.168.0.0/24", "via", "192.168.0.1"])


if __name__ == '__main__':
    unittest.main()
