import logging
import json

import requests

# TODO Add this to typing information
# from controller.logical_port import LogicalPort
logger = logging.getLogger(__name__)


class Container(object):
    def __init__(self, id: str, ip: str, poster: requests) -> None:
        self.id = id
        self.ip = ip
        self.poster = poster
        self.logical_ports = []

    # TODO commented not to use LogicalPort in typing, which currently causes looped imports
    # def add_logical_port(self, port: LogicalPort) -> None:
    def add_logical_port(self, port: LogicalPort) -> None:
        logger.info("Creating logical port on network %s on %s", port.network.ip, self.id)
        data = json.dumps({
                             "net_id": port.network.id,
                             "net_ip": str(port.underlay_network_ip),
                             "router_ip": str(port.router_ip),
                             "ip": str(port.container_ip)},
                        sort_keys=True)
        logging.debug("Sending %s to %s", data, self.ip)
        self.poster.post("http://" + self.ip + ":8090/create/logical_port",
                         headers={"content-type": "application/json"},
                         data=data)
        self.logical_ports.append(port)
