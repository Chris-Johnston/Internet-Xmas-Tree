#!/usr/bin/python
import Configuration
import json
from watchdog.observers import Observer
from watchdog.events import FileSysteEventHandler

import logging
logger = logging.getLogger(__name__)

class WebData(object):

    class FileChangedHandler(FileSysteEventHandler):
        def __init__(self, outer):
            self.outerInstance = outer
        def onMod(self, event):
            print "got file modified"
            outer.fileModified()

    # configuration file from xmasWeb
    config = None
    # thread to handle reading from the file
    readThread = None
    # different parameeters from reading
    color1 = [255,0,0]
    color2 = [0,255,0]
    pattern = 0
    isRandom1 = False
    isRandom2 = False
    length = 10
    delay = 100

    def __init__(self, configuration):
        self.config = configuration
        # get initial values from the file
        fileModified()
        # handlers for changes
        handler = FileChangedHandler(self)
        observer = Observer()
        observer.schedule(handler, path=self.config.DataFile, recursive=False)
        observer.start()

    def close(self):
        observer.stop()
        observer.join()

    def fileModified(self):
        try:
            # open data file
            file = open(self.config.DataFile, "r")
            jsonData = json.load(file)
            # get json data
            self.color1 = jsonData["color1"]
            self.color2 = jsonData["color2"]
            self.pattern = jsonData["pattern"]
            self.isRandom1 = jsonData["isRandom1"]
            self.isRandom2 = jsonData["isRandom2"]
            self.length = jsonData["length"]
            self.delay = jsonData["delay"]
            file.close()
        except Exception as e:
            logger.error("Error: " + e)


