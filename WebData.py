#!/usr/bin/python
from GlobalConfiguration import GlobalConfiguration
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import logging
logger = logging.getLogger(__name__)

class FileChangedHandler(FileSystemEventHandler):
    config = None
    def __init__(self, outer):
        logging.info("HANDLER INIT")
        self.outerInstance = outer
        self.config = outer.config
    def on_modified(self, event):
        logging.info(self.config.DataFile)
        logging.info(event.src_path)
        if self.config.DataFile in event.src_path:
            self.outerInstance.fileModified()

class WebData(object):

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
        self.fileModified()
        # handlers for changes
        handler = FileChangedHandler(self)
        observer = Observer()
        print self.config.DataFile
        observer.schedule(handler, path=self.config.DataPath, recursive=False)
        observer.start()

    def close(self):
        observer.stop()
        observer.join()

    def fileModified(self):
        try:
            logging.info("READING WEB DATA")
            # open data file
            file = open(self.config.DataPath + "/" + self.config.DataFile, "r")
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
            logger.error("Error: " + str(e))
