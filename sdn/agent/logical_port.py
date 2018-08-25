import logging
import subprocess

from enum import Enum
from typing import List
logger = logging.getLogger(__name__)


class CommandExecutor(object):
    @staticmethod
    def execute(cmd: List[str]) -> None:
        logger.debug("Running %s", cmd)
        result = subprocess.run(cmd)
        logging.debug("Result code %d", result.returncode)
        logging.debug("Stdout: %s", result.stdout)
        logging.debug("Stderr: %s", result.stderr)


class LogicalPort(object):
    def __init__(self, net: str, net_ip: str, router_ip: str, local_ip: str) -> None:
        self.net = net
        self.net_ip = net_ip,
        self.router_ip = router_ip
        self.local_ip = local_ip

    def create(self, cmd_executor: CommandExecutor) -> None:
        logger.info("Creating logical port on %s, my IP is %s", self.net, self.local_ip)
        # execute ip route add ...

    def delete(self, cmd_executor: CommandExecutor) -> None:
        logger.info("Deleting logical port on %s", self.net)
        # execute ip route del ...
