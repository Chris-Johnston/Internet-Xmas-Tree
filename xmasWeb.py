#!/usr/bin/env python2.7

# Configuration.py
from GlobalConfiguration import GlobalConfiguration
from WebData import WebData
from DrawThread import DrawThread
from UpdateThread import UpdateThread

# import the rpi_ws281x library
# make sure this is set up first
from neopixel import * 

import logging
# set up logging (I really wanted to call it yule.log)
logging.basicConfig(filename='xmas.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

import colorsys
import math
import time
import random
import threading

# These values shouldn't have to be changed when already working
# moved to configuration file
#LED_COUNT     = 600 # Number of LEDS
LED_PIN     = 18 # GPIO pin connected to the pixels
LED_FREQ_HZ    = 800000 # LED signal frequency in hz
LED_DMA        = 5 # DMA channel for generating signal
# moved to configuration file
#LED_BRIGHTNESS    = 20 # Between 0 and 255, if used with something like 600 leds, have the brightness no more than ~75
LED_INVERT    = False

if __name__ == "__main__":
    # define globals
    global strip
    global stripData
    global config
    global webData
    global updateThread
    global drawThread

    # load the configuration data
    config = GlobalConfiguration()
    config.load()

    #define the strip data
    stripData = [0 for c in range(config.LEDCount)]

    # Create the NeoPixel strip
    strip = Adafruit_NeoPixel(config.LEDCount, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, config.Brightness)
    strip.begin()

    # define web data
    webData = webData(config)

    # Intialize the library (must be called once before other functions).
    strip.begin()

    #start update thread
    updateThread = UpdateThread(stripData, webData, config)

    # start draw thread
    drawThread = DrawThread(stripData, config, strip)

    # loop
    try:
        while True:
            # webData is running when file changes
            # update thread is running
            # draw thread is running
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.debug("End of program")
        webData.close()
        #drawTh.canRun = False        
        #cleanup()
    except Exception as e:
        logger.error("Other exception!" + e)
