"""
Color beams pattern

"""

from .pattern import Pattern

import colorsys
import time

class ColorBeams(Pattern):

    @staticmethod
    def getHue(hue):
        hsv = colorsys.hsv_to_rgb(hue, 1, 1)
        return int(hsv[0] * 255), int(hsv[1] * 255), int(hsv[2] * 255)

    @staticmethod
    def highlight(strip, i, hue = 0.5):
        i = i % len(strip)
        # set the color of this pixel
        strip[i] = ColorBeams.getHue(hue)
        for x in range(15):
            index = (i - x) % len(strip)
            decay = pow(0.7, x)
            # strip[index] = (int(strip[index][0] * decay), int(strip[index][1] * decay), int(strip[index][2] * decay))
            strip[index] = (int(strip[i][0] * decay), int(strip[i][1] * decay), int(strip[i][2] * decay))

    @staticmethod
    def __get_time():
        return time.time() * 1000

    def __init__(self):
        pass
    
    @classmethod
    def get_id(self):
        return 11

    @classmethod
    def update(self, strip, state):
        # use the time to determine the offset
        t = ColorBeams.__get_time()
        offset = int(((t % state.delay) / state.delay) * len(strip))
        for y in range(0, len(strip), 50):
            ColorBeams.highlight(strip, offset + y, (5 * y / len(strip)) % 1)

