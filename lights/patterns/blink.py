"""
Blink Pattern

"""

from .pattern import Pattern

class Blink(Pattern):
    """
    Blink pattern class

    """
    color_toggle = False

    def __init__(self):
        super(Pattern, self).__init__()

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
            strip.fill(list(state.color1))
        else:
            strip.fill(list(state.color2))
        
        self.color_toggle = not self.color_toggle
