"""
Util functions

"""

import random
import colorsys

def get_random_color():
    """
    Gets a random color as a tuple
    """
    hsv = colorsys.hsv_to_rgb(random.random(), 1, 1)
    return int(hsv[0]*255), int(hsv[1]*255), int(hsv[2]*255)