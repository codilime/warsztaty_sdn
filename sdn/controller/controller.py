import docker.types
import netaddr
import ipaddr
import itertools
import logging
import requests

from sdn.controller.logical_port import LogicalPort
from sdn.controller.network import Network
from sdn.controller.router import Router
from sdn.controller.container import Container
from typing import Optional, Sequence

from docker.client import DockerClient

logger = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, router: Router, docker_client: Optional[DockerClient] = None, poster: requests = None) -> None:
        self.router = router
        self.docker_client = docker_client
        self.underlay_subnets = {}
        self.networks = {}
        self.containers = {}
        self.logical_ports = {}
        self.poster = poster

    def clean(self) -> None:
        net_to_delete = list(self.networks.keys())
        for net_id in net_to_delete:
            self.delete_network(net_id)

        self.underlay_subnets = {}
        self.networks = {}
        
        for _, container in self.containers.items():
            container.stop()
        self.containers.clear()

    def _validate_network(self, network: Network) -> None:
        if network.id in self.networks:
            raise RuntimeError('Duplicate network id {net_id}'.format(net_id=network.id))

        try:
            _ = ipaddr.IPNetwork(network.ip)
        except ValueError:
            raise RuntimeError('Invalid CIDR format for network {net_id} - {net_ip}'
                               .format(net_id=network.id, net_ip=network.ip))

        for net_id, net in self.networks.items():
            existing_network = ipaddr.IPNetwork(net.ip)
            new_network = ipaddr.IPNetwork(network.ip)
            if existing_network.overlaps(new_network):
                raise RuntimeError('Specified CIDR for network {new_net_id}-{new_net_ip} overlaps with {ex_net_id}-{ex_net_ip}'
                                   .format(new_net_id=network.id, new_net_ip=network.ip,
                                           ex_net_id=net.id, ex_net_ip=net.ip))

    def add_network(self, network: Network) -> None:
        self._validate_network(network)

        logger.info('Adding network %s', network.ip)
        self._create_underlay_subnets(network)

        self.router.add_network(network)
        self.networks[network.id] = network

    def _create_underlay_subnets(self, overlay_network: Network) -> None:
        self.underlay_subnets[overlay_network.id] = None # store /29 subnets from the overlay_network here

    def delete_network(self, id):
        if id not in self.networks:
            raise RuntimeError('Network with id {net_id} does not exist'.format(net_id=id))

        lp_to_delete = []
        for lp_id, lp in self.logical_ports.items():
            if lp.network.id == id:
                lp_to_delete.append(lp)

        for lp in lp_to_delete:
            self.delete_logical_port(lp)

        self.router.delete_network(self.networks[id])
        del self.networks[id]

    def get_network(self, id: str) -> Network:
        return self.networks[id]

    def list_networks(self) -> Sequence[Network]:
        return list(self.networks.values())

    def add_logical_port(self, port: LogicalPort) -> None:
        logger.info("Adding logical port on %s for %s", port.network.id, port.container.id)
        pool = self._allocate_network_pool(port.network.id)

        self.logical_ports[port.id] = port

    def _allocate_network_pool(self, overlay_network_id: str) -> netaddr.IPNetwork:
        return "192.168.0.8/29"

    def delete_logical_port(self, port: LogicalPort) -> None:
        logger.info("Deleting logical port on %s for %s", port.network.id, port.container.id)

        logger.debug("Notifying router and container")
        port.underlay_network_ip = self.get_network(port.network.id).ip
        port.container.delete_logical_port(port)
        self.router.delete_logical_port(port)

        logger.debug("Deleting underlay docker network")
        underlay_network_name = "{}-{}".format(port.network.id, port.container.id)
        underlay_network = self.docker_client.networks.get(underlay_network_name)
        underlay_network.disconnect(self.router.id)
        underlay_network.disconnect(port.container.id)
        underlay_network.remove()

        del self.logical_ports[port.id]

    def list_logical_ports(self) -> Sequence[LogicalPort]:
        return list(self.logical_ports.values())

    def add_container(self, id: str, code_path: str) -> None:
        container = Container(id=id, poster=self.poster, docker_client=self.docker_client)
        container.start(code_path)
        self.containers[id] = container

    def delete_container(self, id: str) -> None:
        container = self.containers[id]
        container.stop()
        del self.containers[id]

    def get_container(self, id: str) -> Container:
        return self.containers[id]

    def list_containers(self) -> Sequence[Container]:
        return list(self.containers.values())