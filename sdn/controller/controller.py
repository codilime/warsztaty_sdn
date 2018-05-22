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
        self.used_ipam_pools = set()
        self.underlay_networks = {}  # [overlay network name][agent name] is UnderlayNetworkInfo class instance

    def clean(self):
        self.ipam_pools = {}
        self.networks = {}
        # self.used_ipam_pools = set()
        # self.underlay_networks = {}
        for network_id in list(self.underlay_networks):
            for underlay_network_info in list(self.underlay_networks[network_id].values()):
                self.remove_underlay_network(network_overlay_id=network_id, netw_info=underlay_network_info)

    def add_network(self, n):
        logger.info("Adding network %s", n.ip)
        subnets = netaddr.IPNetwork(n.ip).subnet(29)
        self.ipam_pools[n.id] = itertools.cycle(subnets)

        # logger.debug("PPPPPPPPPPPPPPPPPPPP next: %s", list(
        #     (next(self.ipam_pools[n.id] for x in range(0, 20)))
        # ))

        # if n.id in self.underlay_networks:
        #     raise ValueError("Overlay network %s already exists", n.id)

        self.underlay_networks[n.id] = {}
        self.router.add_network(n)
        self.networks[n.id] = n

    def get_network(self, id):
        return self.networks[id]

    def add_logical_port(self, p):
        logger.info("Adding logical port on %s for %s", p.network.id, p.container.id)


        logger.debug("CCCCCCCCC self.used_ipam_pools: %s", list(self.used_ipam_pools))


        #pool = next(self.ipam_pools[p.network.id])
        pool = self.acquire_ipam_pool(overlay_network_id=p.network.id)



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
                                       ipam_pool=pool
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

        self.release_ipam_pool(underlay_network_info=netw_info)

        self.router.remove_logical_port(network_overlay_id, netw_info.router_underlay_ip)
        #port.container.remove_logical_port(port)

        del_netw.disconnect(netw_info.router_id)
        del_netw.disconnect(netw_info.agent_id)

        del_netw.remove()

    def acquire_ipam_pool(self, overlay_network_id):
        first_pool = next(self.ipam_pools[overlay_network_id])
        pool = first_pool

        while True:
            if pool not in self.used_ipam_pools:
                break
            pool = next(self.ipam_pools[overlay_network_id])
            if pool == first_pool:
                raise StopIteration("Run out of ipam pools")
        self.used_ipam_pools.add(pool)
        return pool

    def release_ipam_pool(self, underlay_network_info):
        self.used_ipam_pools.remove(underlay_network_info.ipam_pool)


class UnderlayNetworkInfo(object):
    def __init__(self, network_underlay_id, router_id, router_underlay_ip, agent_id, agent_underlay_ip, ipam_pool):
        #self.overlay_id = network_overlay_id
        self.underlay_id = network_underlay_id
        self.router_id = router_id
        self.router_underlay_ip = router_underlay_ip
        self.agent_id = agent_id
        self.agent_underlay_ip = agent_underlay_ip
        self.ipam_pool = ipam_pool

