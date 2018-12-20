"""
Blink Pattern

"""

from .pattern import Pattern
import time

class Blink(Pattern):
    """
    Blink pattern class

    """
    color_toggle = False
    last_blink_time = 0

    def __init__(self):
        super(Pattern, self).__init__()
        self.__set_time()

    @staticmethod
    def __get_time():
        return time.time() * 1000

    @classmethod
    def __set_time(self):
        self.last_blink_time = Blink.__get_time()

    @classmethod
    def get_id(self):
        """
        Gets the ID of this pattern.
        This is set by the front end, and saved in the data.json. If this ID matches, then this update method will be called.
        """
        return 1

    @classmethod
    def update(self, strip, state):
        """
        Updates the LED strip

        """
        if self.color_toggle:
            strip.fill(state.color1)
        else:
            strip.fill(state.color2)
        if Blink.__get_time() > state.delay + self.last_blink_time:
            self.color_toggle = not self.color_toggle
            self.__set_time()
