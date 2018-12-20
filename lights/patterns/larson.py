"""
"Larson Scanner" pattern
"""

from .pattern import Pattern
import time
import math

class Larson(Pattern):

    def __init__(self):
        super(Pattern, self).__init__()

    @classmethod
    def get_id(self):
        return 6

    @classmethod
    def update(self, strip, state):
        # set all to color2
        strip.fill(state.color2)
        # calculate lit area
        center = len(strip) // 2 + ((len(strip) / 2) - state.length) * math.sin(6.28 * time.time() * 1000.0 / float(state.delay))
        # set the values for the given width
        for x in range(-1 * state.length, state.length + 1):
            # mod by the len of the strip to prevent index out of bound
            strip[int(center + x) % len(strip)] = state.color1