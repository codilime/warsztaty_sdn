import netaddr
import itertools
import logging

logger = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, router, docker_client=None):
        self.router = router
        self.docker_client = docker_client
        self.ipam_pools = {}

    def add_network(self, n):
        logger.info("Adding network %s", n.ip)
        subnets = netaddr.IPNetwork(n.ip).subnet(30)
        self.ipam_pools[n.id] = itertools.islice(subnets, 2) # we've got at most 2 subnets

        self.router.add_network(n)

    def add_logical_port(self, p):
        logger.info("Adding logical port on %s for %s", p.network.id, p.container.id)
        pool = next(self.ipam_pools[p.network.id])
        router_ip, container_ip = pool.iter_hosts()
        logger.info("Allocated %s for router and %s for container", router_ip, container_ip)

        logger.debug("Creating docker networks")
        docker_net = self.docker_client.networks.create(p.network.id)
        docker_net.connect(self.router.id, ipv4_address=router_ip.format())
        docker_net.connect(p.container.id, ipv4_address=container_ip.format())

        logger.debug("Notifying router and container")
        p.router_ip = router_ip
        p.container_ip = container_ip
        self.router.add_logical_port(p)
        p.container.add_logical_port(p)