import logging
from docker import DockerClient as DC
from docker.errors import APIError, NotFound


logger = logging.getLogger('DockerClient')


class DockerClient:
    def __init__(self):
        self.docker_client = DC(base_url='unix://var/run/docker.sock')

    def get_container_ip(self, name):
        try:
            container = self.docker_client.containers.get(name)
            return container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
        except (NotFound, APIError):
            raise RuntimeError(f'Cannot find container {name}')