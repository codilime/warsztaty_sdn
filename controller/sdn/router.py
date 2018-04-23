import urllib.parse


class Router(object):
    def __init__(self, id, ip, poster):
        self.networks = []
        self.id = id
        self.ip = ip
        self.poster = poster
        self.logical_ports = []

    def add_network(self, n):
        self.poster.post(self.ip + "/network", urllib.parse.urlencode({"id": n.id}))
        self.networks.append(n)

    def add_logical_port(self, p):
        self.poster.post(self.ip + "/logical_port", urllib.parse.urlencode({"net_id": p.network.id, "ip":p.router_ip}))
        self.logical_ports.append(p)