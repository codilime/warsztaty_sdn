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
        self.networks = {}  # [overlay network name] is Network class instance
        self.underlay_networks = {}  # [overlay network name, agent name] is UnderlayNetworkInfo class instance

    def clean(self):
        self.ipam_pools = {}
        self.networks = {}

    def add_network(self, n):
        logger.info("Adding network %s", n.ip)
        subnets = netaddr.IPNetwork(n.ip).subnet(29)
        self.ipam_pools[n.id] = itertools.islice(subnets, 3) # we've got at most 2 subnets
        # todo

        # if n.id in self.underlay_networks:
        #     raise ValueError("Overlay network %s already exists", n.id)

        self.underlay_networks[n.id] = {}
        self.router.add_network(n)
        self.networks[n.id] = n

    def get_network(self, id):
        return self.networks[id]

    def add_logical_port(self, p):
        logger.info("Adding logical port on %s for %s", p.network.id, p.container.id)
        pool = next(self.ipam_pools[p.network.id])

        # todo

        hosts = pool.iter_hosts()
        next(hosts) #skip docker default gateway
        router_ip, container_ip = next(hosts), next(hosts)
        logger.info("Allocated %s for router and %s for container from %s pool", router_ip, container_ip, str(pool))

        logger.debug("Creating docker networks")
        ipam = docker.types.IPAMConfig(pool_configs=[docker.types.IPAMPool(subnet=str(pool))])

        docker_net = self.docker_client.networks.create(p.network.id, driver="bridge", ipam=ipam)
        und_netw = UnderlayNetworkInfo(network_underlay_id=docker_net.id,
                                       router_id=self.router.id,
                                       router_underlay_ip=router_ip,
                                       agent_id=p.container.id,
                                       agent_underlay_ip=container_ip,
                                       )
        self.underlay_networks[p.network.id][p.container.id] = und_netw

        docker_net.connect(self.router.id, ipv4_address=router_ip.format())
        docker_net.connect(p.container.id, ipv4_address=container_ip.format())

        logger.debug("Notifying router and container")
        p.router_ip = router_ip
        p.container_ip = container_ip
        p.underlay_network_ip = self.get_network(p.network.id).ip

        self.router.add_logical_port(p)
        p.container.add_logical_port(p)


    def remove_logical_port(self, port):
        logger.info("Removing logical port on %s for %s", port.network.id, port.container.id)
        del_netw_info = self.underlay_networks[port.network.id][port.container.id]

        self.remove_underlay_network(port.network.id, del_netw_info)


    def remove_underlay_network(self, network_overlay_id, netw_info):
        del self.underlay_networks[network_overlay_id][netw_info.agent_id]
        del_netw = self.docker_client.networks.get(network_id=netw_info.underlay_id)

        self.router.remove_logical_port(network_overlay_id, netw_info.router_underlay_ip)
        #port.container.remove_logical_port(port)

        del_netw.disconnect(netw_info.router_id)
        del_netw.disconnect(netw_info.agent_id)

        del_netw.remove()


class UnderlayNetworkInfo(object):
    def __init__(self, network_underlay_id, router_id, router_underlay_ip, agent_id, agent_underlay_ip):
        #self.overlay_id = network_overlay_id
        self.underlay_id = network_underlay_id
        self.router_id = router_id
        self.router_underlay_ip = router_underlay_ip
        self.agent_id = agent_id
        self.agent_underlay_ip = agent_underlay_ip

