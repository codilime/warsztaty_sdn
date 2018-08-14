class Network(object):
    def __init__(self, net_id: str, ip: str) -> None:
        self.id = net_id
        self.ip = ip

    def __eq__(self, other) -> bool:
        return self.id == other.id
