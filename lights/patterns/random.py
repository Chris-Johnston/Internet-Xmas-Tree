"""
Scroll pattern
"""

from .pattern import Pattern
import random

class Scroll(Pattern):

    def __init__(self):
        super(Pattern, self).__init__()

    @classmethod
    def get_id():
        return 2

    @classmethod
    def update(strip, state):
        # set the background to color2
        strip.fill(state.color2)

        for x in range(state.length):
            # pick a random index to set to color1
            index = random.randint(0, len(strip) - 1)
            strip[index] = state.color2