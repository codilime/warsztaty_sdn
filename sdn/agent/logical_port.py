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
        cmd_executor.execute(self._add_route_cmd())

    def delete(self, cmd_executor: CommandExecutor) -> None:
        logger.info("Deleting logical port on %s", self.net)
        cmd_executor.execute(self._del_route_cmd())

    def _add_route_cmd(self) -> List[str]:
        return self._ip_route_cmd(self.IpRouteAction.ADD)

    def _del_route_cmd(self) -> List[str]:
        return self._ip_route_cmd(self.IpRouteAction.DEL)

    class IpRouteAction(Enum):
        ADD = "add"
        DEL = "del"

    def _ip_route_cmd(self, action: IpRouteAction) -> List[str]:
        return ['ip', 'route', action.value, self.net_ip[0], 'via', self.router_ip]
