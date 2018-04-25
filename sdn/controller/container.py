import logging
import json

logger = logging.getLogger(__name__)


class Container(object):
    def __init__(self, id, ip, poster):
        self.id = id
        self.ip = ip
        self.poster = poster
        self.logical_ports = []

    def add_logical_port(self, p):
        logger.info("Creating logical port on network %s on %s", p.network.ip, self.id)
        self.poster.post("http://"+self.ip + ":8090/create/logical_port",
                         headers={"content-type": "application/json"},
                         data=json.dumps({"net_id": p.network.id, "ip": str(p.container_ip)}))
        self.logical_ports.append(p)
