import logging
import psutil

logger = logging.getLogger(__name__)


class InterfaceFinder(object):
    @staticmethod
    def find(ip):
        logger.info("Looking for interface for ip %s", ip)
        if_addrs = psutil.net_if_addrs()
        for iface, addrs in if_addrs.items():
            found = next((addr for addr in addrs if addr.address == ip), None)
            if found is not None:
                logger.info("Interface for %s is %s", ip, iface)
                return iface

        raise RuntimeError(f'No interface for {ip} found')
