import configparser
import os
import logging

logger = logging.getLogger(__file__)

CONFIG_PATH = "config.ini"

config = configparser.SafeConfigParser(os.environ)

try:
    config.read(CONFIG_PATH)
except FileNotFoundError:
    logger.critical("[] Config file not found: %s" % CONFIG_PATH)
