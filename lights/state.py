"""
State Class

Stores information from data read by the json
this is done instead of passing a deserialized dict to objects so that named values
can be used
"""

import os
import json

class State(object):
    """
    Represents the state updated by the API
    """
    # the unix time when the file has been last updated
    last_updated_time = 0
    # the path of the file to read the state from
    file_path = "unset"
    # colors 1 and 2, that must be tuples or lists w/ max value 255
    color1 = (255, 0, 0)
    color2 = (0, 0, 0)
    # if color1/2 are random
    random1 = False
    random2 = False
    # the pattern id to use
    pattern = 0
    # depending on the pattern, typically is how many LEDs
    # wide the pattern is
    length = 5
    # how long in milliseconds the pattern takes to show a difference
    delay = 10

    def __init__(self, file_path):
        self.file_path = file_path
        # load the initial state from the file
        self.__update_state()

    def check_update(self):
        """
        Checks the state file to see if has been updated,
        and if so, reads from the file.
        """
        try:
            time = os.path.getmtime(self.file_path)
            if time > self.last_updated_time:
                # file has been updated since the last time it was read
                self.__update_state()
                self.last_updated_time = time
        except OSError:
            # file not found
            pass

    def __update_state(self):
        """
        Updates the state of this object from the file, called
        when the file is updated.

        Does not perform any validation on the data, only may check
        that the values for types are valid
        """
        # read from the file
        with open(self.file_path) as f:
            data = json.load(f)
            self.color1 = tuple(data['color1'])
            self.color2 = tuple(data['color2'])
            self.random1 = bool(data['random1'])
            self.random2 = bool(data['random2'])
            self.pattern = int(data['pattern'])
            self.length = int(data['length'])
            self.delay = int(data['delay'])
