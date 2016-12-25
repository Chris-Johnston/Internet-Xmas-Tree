#!/usr/bin/env python2.7

# Configuration.py
from GlobalConfiguration import GlobalConfiguration
from ColorUtils import *
from WebData import WebData
import math
#from DrawThread import DrawThread
#from UpdateThread import UpdateThread

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
#LED_COUNT     = 600 # Number of LEDS
LED_PIN     = 18 # GPIO pin connected to the pixels
LED_FREQ_HZ    = 800000 # LED signal frequency in hz
LED_DMA        = 5 # DMA channel for generating signal
# moved to configuration file
#LED_BRIGHTNESS    = 20 # Between 0 and 255, if used with something like 600 leds, have the brightness no more than ~75
LED_INVERT    = False

# fast linear sin approx
def fastApprox(val):
    return 1.0 - math.fabs( math.fmod(val, 2.0) - 1.0)

# globals
#global strip
global stripData
global config
global webData
global updateThread
global drawThread

# start stuff
# load the configuration data
config = GlobalConfiguration()
config.load()

#define the strip data
stripData = [(0,0,0) for c in range(config.LEDCount)]

# Create the NeoPixel strip
strip = Adafruit_NeoPixel(config.LEDCount, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, config.Brightness, strip_type=ws.WS2811_STRIP_GRB)
strip.begin()
# define web data
webData = WebData(config)


# update thread stuff
class UpdateThread(object):

    def __init__(self):
        self.canRun = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.canRun = False

    def run(self):
        while self.canRun:
            try:
                color1 = webData.color1
                color2 = webData.color2
                
                if webData.isRandom1:
                    color1 = hsv(random.random(), 1, 1)
                    #logging.info("RAND C1 " + str(color1))
                if webData.isRandom2:
                    color2 = hsv(random.random(), 1, 1)
                    #logging.info("RAND C2 " + str(color2))
                # this is where I compare the values of web data pattern
                #logging.info(webData.pattern)
                #logging.info(str(config.Patterns))
                #logging.info(str(config.Patterns.get("pattern_solid")))
                # to those in the configuration
                if webData.pattern == int(config.Patterns.get("pattern_solid")):
                    #logging.info("SOLID COLOR")
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
                    #logging.info("BLINK")
                    # set all color 1
                    for x in range(config.LEDCount):
                        stripData[x] = color1
                    # wait
                    time.sleep(webData.delay / 1000.0)
                    #logging.info("BLINK CHANGE")
                    # set all color 2
                    for x in range(config.LEDCount):
                        stripData[x] = color2
                    # wait
                    time.sleep(webData.delay / 1000.0)
                if webData.pattern == int(config.Patterns.get("pattern_scrollsmooth")):
                    #logging.info("Smooth")
                    for x in range(config.LEDCount):
                        c1 = multiplyArray(color1, fastApprox(x / float(webData.length + 1) + float(time.time()) * 1000.0 / float(webData.delay)))
                        c2 = multiplyArray(color2, fastApprox(x / float(webData.length + 1) + 1 + float(time.time()) * 1000.0 / float(webData.delay)))
                        c3 = rgbToTuple(c1[0] + c2[0], c1[1] + c2[1], c1[2] + c2[2])
                        #stripData[x] = addArray(c1, c2)
                        stripData[x] = c3
                if webData.pattern == int(config.Patterns.get("pattern_scroll")):
                    # iterate through
                    for x in range(config.LEDCount):
                        # default color 1
                        color = webData.color1
                        # offset by time, x pos divided by length mod 2
                        # time.time is in seconds not ms
                        # sets color 2
                        if (time.time() / 1000.0 * float(webData.delay) + x / float(webData.length + 1)) % 2 == 1:
                            color = color2
                        # set color
                        stripData[x] = color
                if webData.pattern == int(config.Patterns.get("pattern_wipeup")):
                    # wipe color 1 first
                    for x in range(config.LEDCount):
                        stripData[x] = color1
                        # set the color and wait after each set
                        time.sleep(webData.delay / 1000.0 / float(config.LEDCount))
                    for x in range(config.LEDCount):
                        stripData[x] = color2
                        # set the color and wait after each set
                        time.sleep(webData.delay / 1000.0 / float(config.LEDCount))
                if webData.pattern == int(config.Patterns.get("pattern_wipedown")):
                    # does the same as wipe up but is backwards
                    # wipe color 1 first
                    for x in reversed(range(config.LEDCount)):
                        stripData[x] = color1
                        # set the color and wait after each set
                        time.sleep(webData.delay / 1000.0 / float(config.LEDCount))
                    for x in reversed(range(config.LEDCount)):
                        stripData[x] = color2
                        # set the color and wait after each set
                        time.sleep(webData.delay / 1000.0 / float(config.LEDCount))
                if webData.pattern == int(config.Patterns.get("pattern_random")):
                    #logging.info("RANDOM")
                    # set all to color2
                    for x in range(config.LEDCount):
                        stripData[x] = color2
                    # iterate through length times
                    #logging.info(str(webData.length))
                    for x in range(webData.length):
                        # randomly pick an led and set it to color1
                        i = random.randint(0, config.LEDCount - 1 )
                        #logging.info(str(i))
                        stripData[i] = color1

                    time.sleep(webData.delay / 1000.0)
                if webData.pattern == int(config.Patterns.get("pattern_larson")):
                    #logging.info("larson")
                    # set all to color2
                    for x in range(config.LEDCount):
                        stripData[x] = color2
                    # calculate lit area
                    center = config.LEDCount / 2 + ((config.LEDCount / 2) - webData.length) * math.sin(6.28 * time.time() * 1000.0 / float(webData.delay))
                    #logging.info("center " + str(center))
                    # set the values for the given width
                    for x in range(-1 * webData.length, webData.length):
                        stripData[int(center + x)] = color1

                # for now just set everything to color1
                #for x in range(config.LEDCount):
                #    #logging.info("UPDATE PIXEL " + str(x) + " val " + str( webData.color1));
                #    stripData[x] = webData.color1
            except Exception as e:
                logging.error("Exception " + str(e))

# draw thread stuff
class DrawThread(object):
    def __init__(self):
        self.canRun = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.canRun = False

    def run(self):
        while self.canRun:
            try:
                for x in range(config.LEDCount):
                    try:
                        #logging.info("DRAW RUN")
                        #if(stripData[x] >= 0 and stripData[x] <= (255 << 16 | 255 << 8 | 255)):
                        if True:
                            #logging.info(str(stripData[x]))
                            #logging.info(str(get24BitColorValueArray(stripData[x])))
                            #logging.info("SET PIXEL " + str(x) + "val " + str(int(stripData[x], 16)) + " " + str(stripData[x]))
                            # also clamps
                            strip.setPixelColor(x, get24BitColorValueArray(stripData[x]))
                            #strip.setPixelColor(x, int(stripData[x], 16))
                    except OverflowError:
                        logging.error("Led Overflow error")
                strip.show()
            except Exception as e:
                logging.error("err1" + str(e))

if __name__ == "__main__":
    # Intialize the library (must be called once before other functions).
    strip.begin()

    #start update thread
    updateThread = UpdateThread()

    # start draw thread
    drawThread = DrawThread()

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
