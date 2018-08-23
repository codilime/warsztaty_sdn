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
    def test_should_add_logical_port(self):
        cmds = MockCmdExecutor()
        interfaces = MockInterfaceFinder({"10.0.0.1": "eth0", "10.0.1.1": "eth1"})
        r = Router(cmds, interfaces)

        r.add_network("net1")
        r.add_logical_port("net1", "10.0.0.1")
        r.add_logical_port("net1", "10.0.1.1")

        self.assertListEqual(cmds.commands[0],
                             ['iptables', '-A', 'FORWARD', '-i', 'eth0', '-o', 'eth1', '-j', 'ACCEPT'])
        self.assertListEqual(cmds.commands[1],
                             ['iptables', '-A', 'FORWARD', '-i', 'eth1', '-o', 'eth0', '-j', 'ACCEPT'])

    def test_should_remove_logical_port(self):
        cmds = MockCmdExecutor()
        interfaces = MockInterfaceFinder({"10.0.0.1": "eth0", "10.0.1.1": "eth1"})
        r = Router(cmds, interfaces)

        r.add_network("net1")
        r.add_logical_port("net1", "10.0.0.1")
        r.add_logical_port("net1", "10.0.1.1")

        r.remove_logical_port("net1", "10.0.0.1")

        self.assertListEqual(cmds.commands[2],
                             ['iptables', '-D', 'FORWARD', '-i', 'eth1', '-o', 'eth0', '-j', 'ACCEPT'])
        self.assertListEqual(cmds.commands[3],
                             ['iptables', '-D', 'FORWARD', '-i', 'eth0', '-o', 'eth1', '-j', 'ACCEPT'])

if __name__ == '__main__':
    unittest.main()
