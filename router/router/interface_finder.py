import psutil


class InterfaceFinder(object):
    @staticmethod
    def find(ip):
        if_addrs = psutil.net_if_addrs()
        for iface, addrs in if_addrs.items():
            found = next((addr for addr in addrs if addr.address == ip), None)
            if found is not None:
                return iface
        raise RuntimeError(f'No interface for {ip} found')
