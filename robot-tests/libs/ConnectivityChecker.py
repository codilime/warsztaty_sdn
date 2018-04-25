import logging
import requests


logger = logging.getLogger(__file__)


class ConnectivityChecker(object):

    @staticmethod
    def ping(source_docker_endpoint , target_ip):
        resp = requests.get('http://%s/ping/%s' % (source_docker_endpoint,
                                                   target_ip))
        return int(resp.text) == 1