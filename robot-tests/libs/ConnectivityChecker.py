import logging
import requests


logger = logging.getLogger('ConnectivityChecker')


class ConnectivityChecker:

    @staticmethod
    def ping(source_docker_endpoint , target_ip):
        resp = requests.get(f'http://{source_docker_endpoint}/ping/{target_ip}')
        return int(resp.text) == 1