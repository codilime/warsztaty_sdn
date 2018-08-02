import docker
import docker.errors
import logging
import json

import requests

# TODO Add this to typing information
# from controller.logical_port import LogicalPort
logger = logging.getLogger(__name__)


class Container(object):
    IMAGE = 'sdn-agent'

    def __init__(self, id: str, ip: str, poster: requests) -> None:
        self.id = id
        self.ip = ip
        self.poster = poster
        self.logical_ports = []
        self.docker_client = None

    # TODO commented not to use LogicalPort in typing, which currently causes looped imports
    # def add_logical_port(self, port: LogicalPort) -> None:
    def add_logical_port(self, port) -> None:
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

    def start(self):
        logger.info("Starting %s based on %s image", self.id, Container.IMAGE)
        self.__get_docker_client().containers.run(Container.IMAGE, name=self.id, detach=True, remove=True)

    def stop(self):
        logger.info("Removing containter %s", self.id)
        client = self.__get_docker_client()
        try:
            c = client.containers.get(self.id)
            c.remove(force=True)
        except docker.errors.NotFound:
            logger.info("Container %s already removed", self.id)

    def __get_docker_client(self):
        if self.docker_client is None:
            self.docker_client = docker.from_env()
        return self.docker_client
