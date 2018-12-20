"""
Random pattern
"""

from .pattern import Pattern
import random
import time

class Random(Pattern):
    last_time = 0

    def __init__(self):
        super(Pattern, self).__init__()

    @staticmethod
    def __get_time():
        return time.time() * 1000

    @classmethod
    def __set_time(self):
        self.last_time = Random.__get_time()

    @classmethod
    def get_id(self):
        return 5

    @classmethod
    def update(self, strip, state):
        if Random.__get_time() > (state.delay + self.last_time):
            self.__set_time()
            # set the background to color2
            strip.fill(state.color2)

            for x in range(state.length):
                # pick a random index to set to color1
                index = random.randint(0, len(strip) - 1)
                strip[index] = state.color1