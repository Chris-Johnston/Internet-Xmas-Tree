"""
Pulse pattern
"""

from .pattern import Pattern
import time
import math

class Pulse(Pattern):

    def __init__(self):
        super(Pattern, self).__init__()

    @classmethod
    def get_id(self):
        return 8

    @classmethod
    def update(self, strip, state):
        amp = math.sin(time.time() * 1000.0 / float(state.delay))
        # set the color based on amplitude being negative or pos
        color = state.color1 if amp > 0 else state.color2
        # set the color based on the amplitude
        amp = math.fabs(amp)
        color = (int(amp * color[0]), int(amp * color[1]), int(amp * color[2]))
        # fill the strip with this color
        strip.fill(color)