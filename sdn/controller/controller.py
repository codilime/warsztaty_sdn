import docker.types
import netaddr
import itertools
import logging

logger = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, router, docker_client=None):
        self.router = router
        self.docker_client = docker_client
        self.ipam_pools = {}
        self.networks = {}

    def clean(self):
        self.ipam_pools = {}
        self.networks = {}

    def add_network(self, n):
        logger.info("Adding network %s", n.ip)
        subnets = netaddr.IPNetwork(n.ip).subnet(29)
        self.ipam_pools[n.id] = itertools.islice(subnets, 2) # we've got at most 2 subnets

        self.router.add_network(n)
        self.networks[n.id] = n

    def get_network(self, id):
        return self.networks[id]

    def add_logical_port(self, p):
        logger.info("Adding logical port on %s for %s", p.network.id, p.container.id)
        pool = next(self.ipam_pools[p.network.id])
        hosts = pool.iter_hosts()
        next(hosts) #skip docker default gateway
        router_ip, container_ip = next(hosts), next(hosts)
        logger.info("Allocated %s for router and %s for container from %s pool", router_ip, container_ip, str(pool))

        logger.debug("Creating docker networks")
        ipam = docker.types.IPAMConfig(pool_configs=[docker.types.IPAMPool(subnet=str(pool))])
        docker_net = self.docker_client.networks.create(p.network.id, driver="bridge", ipam=ipam)
        docker_net.connect(self.router.id, ipv4_address=router_ip.format())
        docker_net.connect(p.container.id, ipv4_address=container_ip.format())

        logger.debug("Notifying router and container")
        p.router_ip = router_ip
        p.container_ip = container_ip
        p.underlay_network_ip = self.get_network(p.network.id).ip
        self.router.add_logical_port(p)
        p.container.add_logical_port(p)