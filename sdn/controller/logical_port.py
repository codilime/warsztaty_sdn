# TODO Add this to typing information
# from controller.container import Container
from controller.network import Network


class LogicalPort(object):
    # TODO commented not to use Contaier in typing, which currently causes looped imports
    # def __init__(self, container: Container, network: Network) -> None:
    def __init__(self, container, network: Network) -> None:
        self.container = container
        self.network = network
