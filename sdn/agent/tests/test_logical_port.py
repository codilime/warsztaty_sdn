import unittest
from ..logical_port import LogicalPort


class MockCmdExecutor(object):
    def __init__(self):
        self.commands = []

    def execute(self, cmd):
        self.commands.append(cmd)


class LogicalPortTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
