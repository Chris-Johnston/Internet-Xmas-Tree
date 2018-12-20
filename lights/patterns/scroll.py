"""
Scroll pattern
"""

from .pattern import Pattern
import time
import math

class Scroll(Pattern):

    def __init__(self):
        super(Pattern, self).__init__()

    @classmethod
    def get_id(self):
        return 2

    @classmethod
    def update(self, strip, state):
        # iterate through
        offset = int(time.time() * 1000 / float(state.delay))
        for x in range(len(strip)):
            # default color 1
            color = state.color1
            # offset by time, x pos divided by length mod 2
            # time.time is in seconds not ms
            # sets color 2
            if ((offset + x) // state.length) % 2 == 0:
                color = state.color2
            # set color
            strip[x] = color