"""
Internet-Xmas-Tree

Host program that is responsible for driving the LEDs and updating their patterns.

"""

import config
import neopixel
import board

if __name__ == "__main__":
    conf = config.Config('configuration.ini')
    conf.load()
    
    # initialize the neopixel strip
    # connected to raspberry pi pin 18
    strip = neopixel.NeoPixel(board.D18, conf.count, bpp=3, auto_write=False, brightness=conf.brightness)
    