"""
Lights Client

Responsible for setting the pattern of lights from the data file
"""

import neopixel
import board
import time
import threading
import sys
import inspect
import importlib
from patterns.pattern import Pattern
from config import Config
from state import State

patterns = [
    'patterns.blink',
    'patterns.solid',
    'patterns.traditional',
    'patterns.pulse',
    'patterns.scroll',
    'patterns.scrollsmooth',
    'patterns.random',
    'patterns.larson'
    ]

# todo, need to go back and re-add support for getting random colors

def update(strip, state, pattern_handlers):
    """
    Updates the neopixel state using the dynamically loaded modules from the list of the patterns
    :param strip:
    :return:
    """
    # run the update method for the pattern handler with the matching pattern id
    if state.pattern in pattern_handlers:
        pattern_handlers[state.pattern].update(strip, state)

if __name__ == '__main__':
    # first arg is the path (may be relative) to the config.ini
    config_file = sys.argv[1]
    conf = Config(config_file)
    conf.load()
    
    state = State(conf.data_file)

    # import all the patterns
    pattern_handlers = {}
    for p in patterns:
        # import the module
        mod = importlib.import_module(p)
        # get all of the Pattern subclasses defined inside this module
        for name, obj in inspect.getmembers(mod):
            if obj is not Pattern and isinstance(obj, type) and issubclass(obj, Pattern):
                # append an instance of this class into the handler dict, by the pattern id
                instance = obj()
                pattern_handlers[instance.get_id()] = instance

    # initialize the led strip
    strip = neopixel.NeoPixel(board.D18, conf.count, bpp=3, auto_write=False, brightness=conf.brightness)

    state = None

    try:
        while True:
            # check if data file updated, read from it if it has
            state.check_update()
            # update the state of the led strip
            update(strip, state, pattern_handlers)
            # write the data to the led strip
            strip.show()
            # don't delay at all because the writing process is already slow enough
    except (KeyboardInterrupt, SystemExit):
        # todo proper exception handling
        pass
    except Exception as e:
        pass