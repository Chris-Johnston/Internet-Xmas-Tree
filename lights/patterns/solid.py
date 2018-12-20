"""
Solid Color Pattern

Only displays color 1

"""

# import neopixel
from .pattern import Pattern

class Solid(Pattern):
    """
    Solid pattern class

    """
    
    def __init__(self):
        pass
    
    @classmethod
    def get_id():
        """
        Gets the ID of this pattern.
        This is set by the front end, and saved in the data.json. If this ID matches, then this update method will be called.
        """
        return 0

    @classmethod
    def update(strip, state):
        """
        Updates the LED strip

        """
        strip.fill(state.color1)
