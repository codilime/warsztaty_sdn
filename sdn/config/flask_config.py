import os
from configparser import ConfigParser


CONFIG_FILE = 'global.conf'


def get_config():
    config_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            CONFIG_FILE
        )
    )

    config = ConfigParser()
    config.read(config_path)
    return config