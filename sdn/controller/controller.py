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
        self.underlay_subnets[overlay_network.id] = netaddr.IPNetwork(overlay_network.ip).subnet(29)

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
        router_ip, container_ip = self._allocate_router_and_container_ips(pool)
        logger.info("Allocated %s for router and %s for container from %s pool", router_ip, container_ip, str(pool))

        logger.debug("Creating underlay docker network")
        ipam = docker.types.IPAMConfig(pool_configs=[docker.types.IPAMPool(subnet=str(pool))])
        net_name = "{}-{}".format(port.network.id, port.container.id)
        underlay_network = self.docker_client.networks.create(net_name, driver="bridge", ipam=ipam)
        underlay_network.connect(self.router.id, ipv4_address=router_ip.format())
        underlay_network.connect(port.container.id, ipv4_address=container_ip.format())

        logger.debug("Notifying router and container")
        port.router_ip = router_ip
        port.container_ip = container_ip
        port.underlay_network_ip = self.get_network(port.network.id).ip
        self.router.add_logical_port(port)
        port.container.add_logical_port(port)

        self.logical_ports[port.id] = port

    def _allocate_network_pool(self, overlay_network_id: str) -> netaddr.IPNetwork:
        return next(self.underlay_subnets[overlay_network_id])

    @staticmethod
    def _allocate_router_and_container_ips(pool: netaddr.IPNetwork) -> (netaddr.IPAddress, netaddr.IPAddress):
        hosts = pool.iter_hosts()
        next(hosts)  # skip docker default gateway
        return next(hosts), next(hosts)

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