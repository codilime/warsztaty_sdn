import netaddr
import itertools


class Controller(object):
    def __init__(self, router, docker_client=None):
        self.router = router
        self.docker_client = docker_client
        self.ipam_pools = {}

    def add_network(self, n):
        subnets = netaddr.IPNetwork(n.ip).subnet(30)
        self.ipam_pools[n.id] = itertools.islice(subnets, 2) # we've got at most 2 subnets

        self.router.add_network(n)

    def add_logical_port(self, p):
        pool = next(self.ipam_pools[p.network.id])
        router_ip, container_ip = pool.iter_hosts()

        docker_net = self.docker_client.networks.create(p.network.id)
        docker_net.connect(self.router.id, ipv4_address=router_ip.format())
        docker_net.connect(p.container.id, ipv4_address=container_ip.format())

        p.router_ip = router_ip
        p.container_ip = container_ip
        self.router.add_logical_port(p)
        p.container.add_logical_port(p)