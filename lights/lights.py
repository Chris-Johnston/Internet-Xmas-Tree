"""
Lights Client

Responsible for setting the pattern of lights from the data file
"""

import neopixel
import board
import time`
import threading
import sys
import importlib

# todo dynamically import the following functions, which are patterns
# etc
# import these with importlib.import_module(name)
# patterns = ['blink', 'fade']

def update(strip):
    """
    Updates the neopixel state using the dynamically loaded modules from the list of the patterns
    :param strip:
    :return:
    """
    pass

if __name__ == '__main__':
    # first arg is the path to the web data.json
    # maybe I should be using env vars for this instead
    data_file = sys.argv[1]
    config_file = sys.argv[2]

    config = None

    #todo load the configuration from the config file

    # initialize the led strip
    strip = neopixel.NeoPixel(board.D18, config.LEDCount, bpp=3, auto_write=False, brightness=config.brightness)

    try:
        while True:
            #todo need to use the state of the file if it has changed
            update(strip)
            # write the data to the led strip
            strip.show()
            # don't delay at all because the writing process is already slow enough
            pass
    except (KeyboardInterrupt, SystemExit):
        # todo proper exception handling
        pass
    except Exception as e:
        pass