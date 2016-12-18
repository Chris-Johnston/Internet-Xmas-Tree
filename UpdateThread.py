import WebData
import Configuration
import threading

import logging
logger = logging.getLogger(__name__)

class UpdateThread(object):
    
    def __init__(self, stripData, webData, configurationFile):
        self.strip = stripData
        self.web = webData
        self.config = configurationFile
        self.canRun = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.canRun = False

    def run(self):
        while self.canRun:
            try:
                # for now just set everything to color1
                for x in range(self.config.LEDCount):
                    self.strip[x] = self.web.color1
            except Exception as e:
                logging.error(e)
        