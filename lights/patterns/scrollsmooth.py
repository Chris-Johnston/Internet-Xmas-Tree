"""
Smooth scroll pattern
"""

from .pattern import Pattern
import time
import math

# fast linear sin approx
def fastApprox(val):
    return 1.0 - math.fabs( math.fmod(val, 2.0) - 1.0)

def constrain_int(value):
    return int(min(255, max(value, 0)))

class ScrollSmooth(Pattern):

    def __init__(self):
        super(Pattern, self).__init__()

    @classmethod
    def get_id(self):
        return 7

    @classmethod
    def update(self, strip, state):
        # logging.info("Smooth")
        for x in range(len(strip)):
            c1 = [c * fastApprox(x / float(state.length + 1) + float(time.time()) * 1000.0 / float(state.delay)) for c in state.color1]
            # c2 is out of phase by 1
            c2 = [c * fastApprox(x / float(state.length + 1) + 1 + float(time.time()) * 1000.0 / float(state.delay)) for c in state.color2]
            c3 = tuple(constrain_int(a + b) for a, b in zip(c1, c2))
            strip[x] = c3