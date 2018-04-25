import logging
import time
from docker import DockerClient


logger = logging.getLogger(__file__)


class Cleaner(object):
    def __init__(self):
        self.docker_client = DockerClient(base_url='unix://var/run/docker.sock')

    def remove_network(self, net_name):
        net_to_delete = None
        guard = True

        while guard:
            for net in self.docker_client.networks.list():
                if net.name == net_name:
                    net_to_delete = net
                    break
            else:
                guard = False

            if net_to_delete is None:
                logger.warning('Could not find network to delete %s' % net_name)
                return False

            for container in net_to_delete.containers:
                try:
                    net_to_delete.disconnect(container=container, force=True)
                except:
                    pass
            try:
                net_to_delete.remove()
            except:
                pass
        return True
