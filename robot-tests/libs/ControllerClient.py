import requests
import traceback
import logging
import json
from robot.libraries.BuiltIn import ExecutionFailed
from docker import DockerClient
from docker.errors import NotFound


logger = logging.getLogger('ControllerClient')


class ControllerClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.docker_client = DockerClient(base_url='unix://var/run/docker.sock')

    def _post(self, url_path, data):
        url = f'http://{self.endpoint}/{url_path}'
        headers = {'Content-Type': 'application/json'}

        logger.info(f'Sending request to {url}')
        resp = None
        try:
            resp = requests.post(url=url, headers=headers, data=json.dumps(data))
        except requests.RequestException:
            logger.debug(f'Error during request {url}')
            logger.debug(traceback.format_exc())
            raise RuntimeError('Error during post')
        finally:
            if resp is not None and resp.status_code != 200:
                msg = f'Server responded with error code: {resp.text}'
                logger.debug(msg)
                raise ExecutionFailed(msg)

        logger.info(f'Request success {resp.text}')

    def clean_data(self):
        self._post(url_path='force_clean', data={})

    def create_agent(self, name):
        data = {'id': name}
        self._post(url_path='create/container', data=data)

    def remove_agent(self, name):
        data = {'id': name}
        self._post(url_path='delete/container', data=data)

    def create_network(self, name, cidr):
        data = {'id': name, 'ip': cidr}
        self._post(url_path='create/network', data=data)

    def create_logical_port(self, net_id, docker_id):
        data = {'net_id': net_id,
                'container': {
                    'id': docker_id,
                }}
        self._post(url_path='create/logical_port', data=data)

    def assert_container_exists(self, name):
        try:
            self.docker_client.containers.get(name)
        except NotFound:
            raise RuntimeError(f'Agent {name} does not exist')
        return True