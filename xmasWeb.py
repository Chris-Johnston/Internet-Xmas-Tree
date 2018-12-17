#!/usr/bin/env python3.6

# Configuration.py
from GlobalConfiguration import GlobalConfiguration
from ColorUtils import *
from WebData import WebData
import math

# import the rpi_ws281x library
# make sure this is set up first
from neopixel import *

import logging
# set up logging (I really wanted to call it yule.log)
formatStr = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s"
logging.basicConfig(filename='xmas.log', level=logging.DEBUG, format = formatStr )
logger = logging.getLogger(__name__)

import colorsys
import math
import time
import random
import threading

# These values shouldn't have to be changed when already working
# moved to configuration file
LED_PIN = 18  # GPIO pin connected to the pixels
LED_FREQ_HZ = 800000  # LED signal frequency in hz
LED_DMA = 5  # DMA channel for generating signal
LED_INVERT = False

# fast linear sin approx
def fastApprox(val):
    return 1.0 - math.fabs( math.fmod(val, 2.0) - 1.0)

# globals
global stripData
global config
global webData
global updateThread
global drawThread

# start stuff
# load the configuration data
config = GlobalConfiguration()
config.load()

#define the strip data to all blank
stripData = [(0,0,0) for c in range(config.LEDCount)]

# Create the NeoPixel strip
strip = Adafruit_NeoPixel(
    config.LEDCount, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
    config.Brightness, strip_type=ws.WS2811_STRIP_GRB)
strip.begin()

# define web data
webData = WebData(config)

# update method that will set the values of the strip Data
# this is run before each draw
# set by the webdata
def update():
    try:
        # update the data from the webData
        color1 = webData.color1
        color2 = webData.color2

        if webData.isRandom1:
            color1 = hsv(random.random(), 1, 1)
        if webData.isRandom2:
            color2 = hsv(random.random(), 1, 1)
        # this is where I compare the values of web data pattern
        # logging.info(webData.pattern)
        # logging.info(str(config.Patterns))
        # logging.info(str(config.Patterns.get("pattern_solid")))
        # to those in the configuration
        if webData.pattern == int(config.Patterns.get("pattern_solid")):
            # logging.info("SOLID COLOR")
            # set solid color
            for x in range(config.LEDCount):
                stripData[x] = color1
        if webData.pattern == int(config.Patterns.get("pattern_pulse")):
            amp = math.sin(time.time() * 1000.0 / float(webData.delay))
            color = color1
            if amp < 0:
                color = color2
            color = multiplyArray(color, math.fabs(amp))
            for x in range(config.LEDCount):
                stripData[x] = color
        if webData.pattern == int(config.Patterns.get("pattern_blink")):
            # logging.info("BLINK")
            # set all color 1
            for x in range(config.LEDCount):
                stripData[x] = color1
            draw()
            # wait
            time.sleep(webData.delay / 1000.0)
            # logging.info("BLINK CHANGE")
            # set all color 2
            for x in range(config.LEDCount):
                stripData[x] = color2
            draw()
            # wait
            time.sleep(webData.delay / 1000.0)
        if webData.pattern == int(config.Patterns.get("pattern_scrollsmooth")):
            # logging.info("Smooth")
            for x in range(config.LEDCount):
                c1 = multiplyArray(color1, fastApprox(
                    x / float(webData.length + 1) + float(time.time()) * 1000.0 / float(webData.delay)))
                c2 = multiplyArray(color2, fastApprox(
                    x / float(webData.length + 1) + 1 + float(time.time()) * 1000.0 / float(webData.delay)))
                c3 = rgbToTuple(c1[0] + c2[0], c1[1] + c2[1], c1[2] + c2[2])
                # stripData[x] = addArray(c1, c2)
                stripData[x] = c3
        if webData.pattern == int(config.Patterns.get("pattern_scroll")):
            # iterate through
            offset = int(time.time() * 1000 / float(webData.delay))
            for x in range(config.LEDCount):
                # default color 1
                color = webData.color1
                # offset by time, x pos divided by length mod 2
                # time.time is in seconds not ms
                # sets color 2
                if ((offset + x) / webData.length) % 2 == 1:
                    color = color2
                # set color
                stripData[x] = color
        if webData.pattern == int(config.Patterns.get("pattern_wipeup")):
            # wipe color 1 first
            for x in range(config.LEDCount):
                stripData[x] = color1
                if x%webData.length==0:
                    draw()
                # set the color and wait after each set
                time.sleep(webData.delay / 1000.0 / float(config.LEDCount))
            for x in range(config.LEDCount):
                stripData[x] = color2
                if x%webData.length==0:
                    draw()
                # set the color and wait after each set
                time.sleep(webData.delay / 1000.0 / float(config.LEDCount))
        if webData.pattern == int(config.Patterns.get("pattern_wipedown")):
            # does the same as wipe up but is backwards
            # wipe color 1 first
            for x in reversed(range(config.LEDCount)):
                stripData[x] = color1
                if x%webData.length == 0:
                    draw()
                # set the color and wait after each set
                time.sleep(webData.delay / 1000.0 / float(config.LEDCount))
            for x in reversed(range(config.LEDCount)):
                stripData[x] = color2
                if x%webData.length == 0:
                    draw()
                # set the color and wait after each set
                time.sleep(webData.delay / 1000.0 / float(config.LEDCount))

        if webData.pattern == int(config.Patterns.get("pattern_random")):
            # logging.info("RANDOM")
            # set all to color2
            for x in range(config.LEDCount):
                stripData[x] = color2
            # iterate through length times
            # logging.info(str(webData.length))
            for x in range(webData.length):
                # randomly pick an led and set it to color1
                i = random.randint(0, config.LEDCount - 1)
                # logging.info(str(i))
                stripData[i] = color1

            time.sleep(webData.delay / 1000.0)
        if webData.pattern == int(config.Patterns.get("pattern_larson")):
            # set all to color2
            for x in range(config.LEDCount):
                stripData[x] = color2
            # calculate lit area
            center = config.LEDCount / 2 + ((config.LEDCount / 2) - webData.length) * math.sin(
                6.28 * time.time() * 1000.0 / float(webData.delay))
            # logging.info("center " + str(center))
            # set the values for the given width
            for x in range(-1 * webData.length, webData.length):
                stripData[int(center + x)] = color1
        # catch exceptions in the updates
    except Exception as e:
        logging.error("Exception when updating " + str(e))

def draw():
    try:
        for x in range(config.LEDCount):
            strip.setPixelColor(x, get24BitColorValueArray(stripData[x]))
        strip.show()
    except Exception as e:
        logging.error("Error when drawing " + str(e))

if __name__ == "__main__":
    # Intialize the library (must be called once before other functions).
    strip.begin()

    # loop
    try:
        while True:
            # webData is running when file changes
            # update the values
            update()
            # draw the values
            draw()

            time.sleep(0.001)

            # update the values of the strip


    except (KeyboardInterrupt, SystemExit):
        logger.debug("End of program")
        webData.close()
    except Exception as e:
        logger.error("Other exception!" + e)
