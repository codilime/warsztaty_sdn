import docker.types
import netaddr
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
        self.ipam_pools = {}
        self.networks = {}
        self.containers = {}
        self.logical_ports = []
        self.poster = poster

    def clean(self) -> None:
        self.ipam_pools = {}
        self.networks = {}
        for _, container in self.containers.items():
            container.stop()
        self.containers.clear()

    def add_network(self, network: Network) -> None:
        if network.id in self.networks:
            raise RuntimeError('Duplicate network id {network}'.format(network=network.id))

        logger.info("Adding network %s", network.ip)
        subnets = netaddr.IPNetwork(network.ip).subnet(29)
        self.ipam_pools[network.id] = itertools.islice(subnets, 2)  # we've got at most 2 subnets

        self.router.add_network(network)
        self.networks[network.id] = network

    def get_network(self, id: str) -> Network:
        return self.networks[id]

    def list_networks(self) -> Sequence[Network]:
        return list(self.networks.values())

    def add_logical_port(self, port: LogicalPort) -> None:
        logger.info("Adding logical port on %s for %s", port.network.id, port.container.id)
        pool = next(self.ipam_pools[port.network.id])
        hosts = pool.iter_hosts()
        next(hosts)  # skip docker default gateway
        router_ip, container_ip = next(hosts), next(hosts)
        logger.info("Allocated %s for router and %s for container from %s pool", router_ip, container_ip, str(pool))

        logger.debug("Creating underlay docker network")
        ipam = docker.types.IPAMConfig(pool_configs=[docker.types.IPAMPool(subnet=str(pool))])
        net_name = "{}-{}".format(port.network.id, port.container.id)
        docker_net = self.docker_client.networks.create(port.network.id, driver="bridge", ipam=ipam, name=net_name)
        docker_net.connect(self.router.id, ipv4_address=router_ip.format())
        docker_net.connect(port.container.id, ipv4_address=container_ip.format())

        logger.debug("Notifying router and container")
        port.router_ip = router_ip
        port.container_ip = container_ip
        port.underlay_network_ip = self.get_network(port.network.id).ip
        self.router.add_logical_port(port)
        port.container.add_logical_port(port)

        self.logical_ports.append(port)

    def delete_logical_port(self, port: LogicalPort) -> None:
        logger.info("Deleting logical port on %s for %s", port.network.id, port.container.id)

        logger.debug("Notifying router and container")
        port.underlay_network_ip = self.get_network(port.network.id).ip
        port.container.delete_logical_port(port)
        self.router.delete_logical_port(port)

        logger.debug("Deleting underlay docker network")
        net_name = "{}-{}".format(port.network.id, port.container.id)
        docker_net = self.docker_client.networks.get(net_name)
        docker_net.disconnect(self.router.id)
        docker_net.disconnect(port.container.id)
        docker_net.remove()

        self.logical_ports.remove(port)

    def list_logical_ports(self) -> Sequence[LogicalPort]:
        return self.logical_ports

    def add_container(self, id: str, code_path: str) -> None:
        container = Container(id=id, poster=self.poster, docker_client=self.docker_client)
        container.start(code_path)
        self.containers[id] = container

    def remove_container(self, id: str) -> None:
        container = self.containers[id]
        container.stop()
        del self.containers[id]

    def get_container(self, id: str) -> Container:
        return self.containers[id]

    def list_containers(self) -> Sequence[Container]:
        return list(self.containers.values())