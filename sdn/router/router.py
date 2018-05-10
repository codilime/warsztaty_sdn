import logging
import subprocess

logger = logging.getLogger(__name__)


class Router(object):

    def __init__(self, command_executor, interface_finder):
        self.command_executor = command_executor
        self.interface_finder = interface_finder
        self.networks = {}

    def add_network(self, name):
        logger.info("Adding network %s", name)
        self.networks[name] = []

    def add_logical_port(self, net, ip):
        logger.info("Adding logical port %s/%s", net, ip)
        my_interface = self.interface_finder.find(ip)
        for peer in self.networks[net]:
            peer_interface = self.interface_finder.find(peer)
            logger.debug("Configuring routing for %s <-> %s", my_interface, peer_interface)
            self.command_executor.execute(self._build_forward_command(peer_interface, my_interface))
            self.command_executor.execute(self._build_forward_command(my_interface, peer_interface))

        self.networks[net].append(ip)

    def remove_logical_port(self, net, ip):
        logger.info("Removing logical port %s/%s", net, ip)
        my_interface = self.interface_finder.find(ip)
        for peer in self.networks[net]:
            peer_interface = self.interface_finder.find(peer)
            logger.debug("Removing routing for %s <-> %s", my_interface, peer_interface)
            self.command_executor.execute(self._build_forward_command(peer_interface, my_interface, False))
            self.command_executor.execute(self._build_forward_command(my_interface, peer_interface, False))

        self.networks[net].remove(ip)

    @staticmethod
    def _build_forward_command(iface_in, iface_out, add=True):
        return ['iptables', '-A' if add else '-D', 'FORWARD', '-i', iface_in, '-o', iface_out, '-j', 'ACCEPT']


class CommandExecutor(object):
    @staticmethod
    def execute(cmd):
        subprocess.run(cmd)