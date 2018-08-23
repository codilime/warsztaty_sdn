import json
import logging

import requests
from sdn.controller.logical_port import LogicalPort
from sdn.controller.network import Network

logger = logging.getLogger(__name__)


class Router(object):
    def __init__(self, id: str, ip: str, poster: requests) -> None:
        self.networks = []
        self.id = id
        self.ip = ip
        self.poster = poster
        self.logical_ports = []

    def add_network(self, n: Network) -> None:
        logger.info("Creating network %s", n.id)
        self.poster.post(self.ip + "/create/network",
                         headers={"content-type": "application/json"},
                         data=json.dumps({"name": n.id}))
        self.networks.append(n)

    def add_logical_port(self, p: LogicalPort) -> None:
        logger.info("Creating logical port on %s", p.network.id)
        self.poster.post(self.ip + "/create/logical_port",
                         headers={"content-type": "application/json"},
                         data=json.dumps({"name": p.network.id, "ip": str(p.router_ip)}, sort_keys=True))
        self.logical_ports.append(p)

    def delete_logical_port(self, p: LogicalPort) -> None:
        logger.info("Deleting logical port on %s", p.network.id)
        self.poster.delete(self.ip + "/logical_port",
                         headers={"content-type": "application/json"},
                         data=json.dumps({"name": p.network.id, "ip": str(p.router_ip)}, sort_keys=True))
        self.logical_ports.remove(p)
