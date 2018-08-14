import logging
import subprocess
from typing import List, Type

from .interface_finder import InterfaceFinder

logger = logging.getLogger(__name__)


class CommandExecutor(object):
    @staticmethod
    def execute(cmd):
        subprocess.run(cmd)


class Router(object):

    def __init__(self, command_executor: Type[CommandExecutor], interface_finder: Type[InterfaceFinder]) -> None:
        self.command_executor = command_executor
        self.interface_finder = interface_finder
        self.networks = {}

    def add_network(self, name: str) -> None:
        logger.info("Adding network %s", name)
        self.networks[name] = []

    def add_logical_port(self, net: str, ip: str) -> None:
        logger.info("Adding logical port %s/%s", net, ip)
        my_interface = self.interface_finder.find(ip)
        for peer in self.networks[net]:
            peer_interface = self.interface_finder.find(peer)
            logger.debug("Configuring routing for %s <-> %s", my_interface, peer_interface)
            self.command_executor.execute(self._build_forward_command(peer_interface, my_interface))
            self.command_executor.execute(self._build_forward_command(my_interface, peer_interface))

        self.networks[net].append(ip)

    @staticmethod
    def _build_forward_command(iface_in: str, iface_out: str) -> List[str]:
        return ['iptables', '-A', 'FORWARD', '-i', iface_in, '-o', iface_out, '-j', 'ACCEPT']
