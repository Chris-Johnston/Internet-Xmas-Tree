import Configuration
import threading

import logging
logger = logging.getLogger(__name__)

class DrawThread(object):
    def __init__(self, stripData, configuration, NeopixelStrip):
        self.config = configuration
        self.stripData = stripData
        self.strip = NeopixelStrip
        self.canRun = True

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.canRun = False

    def run(self):
        while self.canRun:
            try:
                for x in range(self.config.LEDCount):
                    try:
                        if(stripData[x] >= 0 and stripData[x] <= (255 << 16 | 255 << 8 | 255)):
                            self.strip.setPixelColor(x, self.stripData[x])
                    except OverflowError:
                        logging.error("Led Overflow error")
                self.strip.show()
            except Exception as e:
                logging.error(e)
        