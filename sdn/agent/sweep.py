import logging
import subprocess

logger = logging.getLogger(__name__)


class PingSweep(object):
    @staticmethod
    def sweep(target: str) -> int:
        logger.info("Checking availability of %s", target)
        result = subprocess.run(['ping', '-c1', target])
        logging.debug('Stdout: %s', result.stdout)
        logging.debug('Stderr: %s', result.stderr)
        return 1 if result.returncode == 0 else 0
