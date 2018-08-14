# TODO Add this to typing information
# from controller.container import Container
from sdn.controller.network import Network


class LogicalPort(object):
    # TODO commented not to use Contaier in typing, which currently causes looped imports
    # def __init__(self, container: Container, network: Network) -> None:
    def __init__(self, container, network: Network) -> None:
        self.container = container
        self.network = network

        # Will be filled in later
        self.router_ip: str = None
        self.container_ip: str = None
        self.underlay_network_ip: str = None

    def __eq__(self, other) -> bool:
        return self.container == other.container and self.network == other.network