import unittest
from ..router import Router


class MockCmdExecutor(object):
    def __init__(self):
        self.commands = []

    def execute(self, cmd):
        self.commands.append(cmd)


class MockInterfaceFinder(object):
    def __init__(self, interfaces):
        self.interfaces = interfaces

    def find(self, ip):
        return self.interfaces[ip]


class RouterTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
