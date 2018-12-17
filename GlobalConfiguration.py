import configparser

import logging
logger = logging.getLogger(__name__)


class GlobalConfiguration(object):
    Patterns = {}
    LEDCount = 600
    Brightness = 20
    DataFile = ""
    DataPath = ""

    def __init__(self, **kwargs):
        self.Brightness = 30
        self.LEDCount = 600
        self.DataFile = ""
        self.DataPath = ""
        self.Patterns = {}

    def load(self):
        c = configparser.ConfigParser()
        # this must be in the same directory
        # when starting the program, cd first
        c.read("configuration.ini")

        try:
           self.Brightness = int( c.get("Configuration", "LED_BRIGHTNESS"))
           self.LEDCount = int( c.get("Configuration", "NUMBER_OF_LEDS"))
           self.DataFile = c.get("Configuration", "DATA_FILE")
           self.DataPath = c.get("Configuration", "DATA_PATH")
           self.Patterns = dict(c.items("Patterns"))
        except Exception as e:
            logger.error("Couldn't fetch configuration information. " + str(e))
    
