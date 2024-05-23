"""
    The confReader, just as the name presumes will read the config.yaml file.
"""

import yaml
from initConf import initConfig
from ..logUtils import logger


class confReader:
    def __init__(self):
        self.directory_path = "~/.config/TWM/"
        self.config_path = self.directory_path + "config.yaml"
        self.read()

    def read(self):
        try:
            if initConfig.checkConf():
                with open(self.config_path) as f:
                    config = yaml.safe_load(f)
                    return config
        finally:
            logger.info("Config File found... started reading")
