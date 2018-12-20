"""
"Traditional" xmas tree lights
lights that just stay static based on the index of the led
don't animate or anything
"""

from .pattern import Pattern
import random

class Traditional(Pattern):
    """
    "Traditional" lights pattern
    """
    colors = [
        # red
        (255, 0, 0),
        # green
        (0, 255, 0),
        # blue
        (0, 0, 255),
        # orange
        (255, 153, 0),
        # pink
        (255, 51, 153),
        # cyan
        (0, 255, 255),
        # yellow
        (255, 255, 102)
    ]

    def __init__(self):
        super(Pattern, self).__init__()
        # shuffle the random colors on init, so that they aren't in the 
        # same order that they are in code
        random.shuffle(self.colors)

    @classmethod
    def get_id(self):
        return 9

    @classmethod
    def update(self, strip, state):
        # set all of the strip colors to be one of the preset colors
        strip.fill((0, 0, 0))
        for index in range(0, len(strip), 2):
            strip[index] = self.colors[index % len(self.colors)]
