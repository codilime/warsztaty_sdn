import urllib.parse


class Container(object):
    def __init__(self, id, ip, poster):
        self.id = id
        self.ip = ip
        self.poster = poster
        self.logical_ports = []

    def add_logical_port(self, p):
        self.poster.post(self.ip + "/logical_port", urllib.parse.urlencode({"net_ip": p.network.ip}))
        self.logical_ports.append(p)