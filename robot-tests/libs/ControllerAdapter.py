import requests
import traceback
import logging
import json
from robot.libraries.BuiltIn import ExecutionFailed


logger = logging.getLogger(__file__)


class ControllerAdapter(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def _post(self, url_path, data):
        url = 'http://%s/%s' % (self.endpoint, url_path)
        headers = {'Content-Type': 'application/json'}

        logger.info('Sending request to %s' % url)
        resp = None
        try:
            resp = requests.post(url=url, headers=headers, data=json.dumps(data))
        except requests.RequestException:
            logger.error('Error during request %s' % url)
            logger.error(traceback.format_exc())
            return
        finally:
            if resp is not None and resp.status_code != 200:
                msg ='Server responded with error code: %s' % str(resp.text)
                logger.error(msg)
                raise ExecutionFailed(msg)

        logger.info('Request success %s' % resp.text)

    def create_network(self, name, cidr):
        data = {'name': name, 'cidr': cidr}
        self._post(url_path='create/network', data=data)

    def create_logical_port(self, net_id, docker_id, docker_ip):
        data = {'net_id': net_id,
                'container': {
                    'id': docker_id,
                    'ip': docker_ip
                }}
        self._post(url_path='create/logical_port', data=data)