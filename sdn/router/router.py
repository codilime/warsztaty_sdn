import logging
import subprocess
from typing import List, Type
from enum import Enum

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
        logger.info("Adding network %s" % name)
        self.networks[name] = []

    def remove_network(self, name: str) -> None:
        logger.info("Removing network %s" % name)
        if name in self.networks:
            del self.networks[name]
        else:
            logger.warning('No %s network for removal' % name)

    def add_logical_port(self, net: str, ip: str) -> None:
        logger.info("Adding logical port %s/%s" % (net, ip))
        # execute iptables -A FORWARD -i ethX -o ethY -j ACCEPT for all interface pairs in the overlay network

        self.networks[net].append(ip)

    def remove_logical_port(self, net: str, ip: str) -> None:
        logger.info("Removing logical port %s/%s" % (net, ip))
        # execute iptables -D FORWARD -i ethX -o ethY -j ACCEPT for all interface pairs in the overlay network
