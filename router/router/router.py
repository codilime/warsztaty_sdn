class Router(object):
    FORWARD_COMMAND = 'iptables -A FORWARD -i {} -o {} -j ACCEPT'

    def __init__(self, command_executor, interface_finder):
        self.command_executor = command_executor
        self.interface_finder = interface_finder
        self.networks = {}

    def add_network(self, name):
        self.networks[name] = []

    def add_logical_port(self, net, ip):
        my_interface = self.interface_finder.find(ip)
        for peer in self.networks[net]:
            peer_interface = self.interface_finder.find(peer)
            self.command_executor.execute(self.FORWARD_COMMAND.format(peer_interface, my_interface))
            self.command_executor.execute(self.FORWARD_COMMAND.format(my_interface, peer_interface))

        self.networks[net].append(ip)