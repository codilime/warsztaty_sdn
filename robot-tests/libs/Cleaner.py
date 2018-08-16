import logging
from docker import DockerClient
from docker.errors import APIError, NotFound


logger = logging.getLogger('Cleaner')


class Cleaner:
    def __init__(self):
        self.docker_client = DockerClient(base_url='unix://var/run/docker.sock')

    def remove_network(self, net_name):
        if not net_name:
            return True

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
                logger.debug('Could not find network to delete %s' % net_name)
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

    def remove_agent(self, agent_name):
        if not agent_name:
            return True

        try:
            pass
            # container = self.docker_client.containers.get(agent_name)
            # container.remove(force=True)
        except (NotFound, APIError):
            raise RuntimeError(f'Could not remove {agent_name}')