"""
    initConf's main function is to check and see if the config file is made in ~/.config/TWM including the directory
    if the directory or the file do not exist, then they will be created.
"""

from twm.utils.logUtils import logger
import os


class initConfig:
    def __init__(self):
        self.directory_path = "~/.config/TWM/"
        self.config_path = self.directory_path + "config.yaml"
        self.createDir()
        self.createConf()

    def checkConf(self):
        logger.info("Checking for Config File or Directory Existence")
        if not os.path.exists(self.config_path) and not os.path.exists(self.directory_path):
            if not os.path.exists(self.directory_path):
                logger.critical("Directory does not exist.")
                self.createDir()
            elif not os.path.exists(self.config_path):
                logger.critical("Config File does not exist.")
                self.createConf()
        else:
            logger.info("Directory and Config File Exist.")

    def createDir(self):
        logger.info("Creating Directory_Path...")
        try:
            os.makedirs(self.directory_path)
        except FileExistsError:
            logger.error(f"Directory '{self.directory_path}' already exists.")
        except PermissionError:
            logger.error(f"Permission denied while creating directory '{self.directory_path}'.")
        except OSError as e:
            logger.error(f"Failed to create directory '{self.directory_path}': {e}")
        finally:
            logger.info(f"Successfully created {self.directory_path}")

    def createConf(self):
        logger.info("Creating Config_Path...")
        try:
            with open(self.config_path, 'w'):
                pass
        except FileExistsError:
            logger.error(f"File '{self.config_path}' already exists")
        except PermissionError:
            logger.error(f"Permission denied while creating file '{self.config_path}'.")
        except OSError as e:
            logger.error(f"Failed to create file '{self.config_path}': {e}")
        finally:
            logger.error(f"Successfully created {self.config_path}")
