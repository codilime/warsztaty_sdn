import json


class Router(object):
    def __init__(self, id, ip, poster):
        self.networks = []
        self.id = id
        self.ip = ip
        self.poster = poster
        self.logical_ports = []

    def add_network(self, n):
        self.poster.post(self.ip + "/create/network",
                         headers={"content-type": "application/json"},
                         data=json.dumps({"id": n.id}))
        self.networks.append(n)

    def add_logical_port(self, p):
        self.poster.post(self.ip + "/create/logical_port",
                         headers={"content-type": "application/json"},
                         data=json.dumps({"net_id": p.network.id, "ip":p.router_ip}))
        self.logical_ports.append(p)