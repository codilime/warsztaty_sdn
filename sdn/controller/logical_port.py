from controller.container import Container
from controller.network import Network


class LogicalPort(object):
    def __init__(self, container: Container, network: Network) -> None:
        self.container = container
        self.network = network
