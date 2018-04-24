import logging
import re
import subprocess

logger = logging.getLogger(__name__)


class PingSweep(object):
    SWEEP_CMD = 'sudo nmap -v -sn -PE -n -oG - %s'
    HOSTS_UP = re.compile(r"([0-9]+) host(s)? up")

    def sweep(self, target):
        logger.info("Starting network sweep on %s", target)
        output = self.exec_command(self.SWEEP_CMD % target)

        logger.debug("Sweep result: %s", output)
        if not output:
            return 0

        match = self.HOSTS_UP.search(output)
        if not match:
            return 0

        if len(match.groups()) > 0:
            return int(match.groups()[0])
        else:
            return 0

    @staticmethod
    def exec_command(cmd):
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True).stdout.read().decode('utf-8')
