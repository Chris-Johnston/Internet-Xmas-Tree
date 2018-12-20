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
    def get_id():
        """
        Gets the ID of this pattern.
        This is set by the front end, and saved in the data.json. If this ID matches, then this update method will be called.
        """
        return 1

    @classmethod
    def update(strip, state):
        """
        Updates the LED strip

        """
        if color_toggle:
            strip.fill(state.color1)
        else:
            strip.fill(state.color2)
        
        color_toggle = not color_toggle
