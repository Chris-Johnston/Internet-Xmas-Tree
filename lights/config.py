"""
Configuration Object

Stores information about the configuration, 
as parsed from the configuration file.
"""

import configparser

class Config(object):
    patterns = {}
    count = 600
    brightness = 0.2
    config_file = ""
    data_file = ""
    
    def __init__(self, config_file, **kwargs):
        """
        Constructor
        """
        self.config_file = config_file

    def load(self):
        """
        Loads information from the config file specified.
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)

        self.brightness = float(config['Configuration']['LED_BRIGHTNESS'])
        self.count = float(config['Configuration']['NUMBER_OF_LEDS'])
        self.data_file = config['Configuration']['DATA_FILE']
