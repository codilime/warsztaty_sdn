import logging
import urllib.parse

logger = logging.getLogger(__name__)


class Container(object):
    def __init__(self, id, ip, poster):
        self.id = id
        self.ip = ip
        self.poster = poster
        self.logical_ports = []

    def add_logical_port(self, p):
        logger.info("Creating logical port on network %s on %s", p.network.ip, self.id)
        self.poster.post(self.ip + "/logical_port", urllib.parse.urlencode({"net_ip": p.network.ip, "ip": p.container_ip}))
        self.logical_ports.append(p)
