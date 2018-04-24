import logging


logger = logging.getLogger(__name__)


class LogicalPort(object):
    def __init__(self, net, local_ip):
        self.net = net
        self.local_ip = local_ip

    def create(self, cmd_executor):
        logger.info("Creating logical port on %s, my IP is %s", self.net, self.local_ip)
        cmd_executor.execute(['route', 'add', 'default', 'gw', self.local_ip])