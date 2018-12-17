import neopixel
import board
import time
import random
import colorsys

def getHue(hue):
    hsv = colorsys.hsv_to_rgb(hue, 1, 1)
    return int(hsv[0] * 255), int(hsv[1] * 255), int(hsv[2] * 255)


def getRandomColor():
    hsv = colorsys.hsv_to_rgb(random.random(), 1, 1)
    return int(hsv[0]*255), int(hsv[1]*255), int(hsv[2]*255)


def highlight(strip, i, hue = 0.5):
    i = i % len(strip)
    # set the color of this pixel
    strip[i] = getHue(hue)
    for x in range(20):
        index = (i - x) % len(strip)
        decay = pow(0.7, x)
        # strip[index] = (int(strip[index][0] * decay), int(strip[index][1] * decay), int(strip[index][2] * decay))
        strip[index] = (int(strip[i][0] * decay), int(strip[i][1] * decay), int(strip[i][2] * decay))

with neopixel.NeoPixel(board.D18, 600, bpp=3, auto_write=False, brightness=0.1) as strip:
    while True:
        for i in range(len(strip)):
            for y in range(0, len(strip), 50):
                highlight(strip, i + y, (5 * y / len(strip)) % 1)
            if i % 1 == 0:
                strip.show()
        time.sleep(0.1)

