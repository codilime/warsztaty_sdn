class LogicalPort(object):
    def __init__(self, net, local_ip):
        self.net = net
        self.local_ip = local_ip

    def create(self, cmd_executor):
        cmd_executor.execute(['route', 'add', 'default', 'gw', self.local_ip])