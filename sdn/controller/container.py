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
        data = json.dumps({
                             "net_id": p.network.id,
                             "net_ip": str(p.underlay_network_ip),
                             "router_ip": str(p.router_ip),
                             "ip": str(p.container_ip)},
                        sort_keys=True)
        logging.debug("Sending %s to %s", data, self.ip)
        self.poster.post("http://"+self.ip + ":8090/create/logical_port",
                         headers={"content-type": "application/json"},
                         data=data)
        self.logical_ports.append(p)

    def remove_logical_port(self, p):
        logger.info("Removing logical port on network %s on %s", p.network.ip, self.id)
        data = json.dumps({
            "net_id": p.network.id,
            "net_ip": str(p.underlay_network_ip),
            "router_ip": str(p.router_ip),
            "ip": str(p.container_ip)},
            sort_keys=True)

        self.poster.post("http://" + self.ip + ":8090/remove/logical_port",
                         headers={"content-type": "application/json"},
                         data=data)

        for port in self.logical_ports:
            if port.network.id == p.network.id and port.container_ip == p.container_ip:
                self.logical_ports.remove(port)
                break
