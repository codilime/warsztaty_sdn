import json
import logging

import docker
import docker.errors
import requests
import os

# TODO Add this to typing information
# from controller.logical_port import LogicalPort
logger = logging.getLogger(__name__)


class Container(object):
    IMAGE = 'agent'

    def __init__(self, id: str, poster: requests, docker_client: docker.DockerClient) -> None:
        self.id = id
        self.ip = ''
        self.poster = poster
        self.logical_ports = []
        self.docker_client = docker_client

    def __eq__(self, other) -> bool:
        return self.id == other.id

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

    def start(self, code_path: str) -> None:
        abs_code_path = os.path.abspath(code_path)
        logger.info("Starting %s based on %s image with code in %s", self.id, Container.IMAGE, abs_code_path)
        self.docker_client.containers.run(Container.IMAGE, name=self.id, detach=True, remove=True,
                                          volumes={abs_code_path: {'bind': '/opt/sdn', 'mode': 'ro'}})
        c = self.docker_client.containers.get(self.id)
        self.ip = c.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]

    def stop(self) -> None:
        logger.info("Removing container %s", self.id)
        try:
            c = self.docker_client.containers.get(self.id)
            c.remove(force=True)
        except docker.errors.NotFound:
            logger.info("Container %s already removed", self.id)
