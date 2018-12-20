"""
WipeDown Pattern

"""

from .pattern import Pattern
import time

class WipeDown(Pattern):
    """
    WipeDown pattern class

    """
    def __init__(self):
        super(Pattern, self).__init__()

    @staticmethod
    def __get_time():
        return time.time() * 1000
    @classmethod
    def get_id(self):
        """
        Gets the ID of this pattern.
        This is set by the front end, and saved in the data.json. If this ID matches, then this update method will be called.
        """
        return 4

    @classmethod
    def update(self, strip, state):
        """
        Updates the LED strip

        """
        t = WipeDown.__get_time()

        primary = state.color1
        secondary = state.color2

        # based on this time, determines how far the wipe is, and what the background color is
        if (t // state.delay) % 2 == 0:
            primary = state.color2
            secondary = state.color1
        # how far along the wipe has "completed"
        completed = (t % state.delay) / state.delay
        completed_pixel = int(len(strip) * completed)
        # fill the strip
        strip.fill(secondary)
        for idx in range(completed_pixel):
            strip[len(strip) - 1 - idx] = primary