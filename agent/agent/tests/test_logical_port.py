import unittest
from agent.logical_port import LogicalPort


class MockCmdExecutor(object):
    def __init__(self):
        self.commands = []

    def execute(self, cmd):
        self.commands.append(cmd)


class LogicalPortTest(unittest.TestCase):
    def test_should_add_default_route(self):
        mock_cmd = MockCmdExecutor()
        p = LogicalPort("192.168.0.0/24", "192.168.0.2")

        p.create(mock_cmd)

        self.assertListEqual(mock_cmd.commands[0], ["route", "add", "default", "gw", "192.168.0.2"])


if __name__ == '__main__':
    unittest.main()
