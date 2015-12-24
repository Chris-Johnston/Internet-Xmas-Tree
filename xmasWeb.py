# xmasWeb.py

import colorsys
import math
import time
import random
import threading
from neopixel import * # import the rpi_ws281x library

LED_COUNT 	= 600 # Number of LEDS
LED_PIN 	= 18 # GPIO pin connected to the pixels
LED_FREQ_HZ	= 800000 # LED signal frequency in hz
LED_DMA		= 5 # DMA channel for generating signal
LED_BRIGHTNESS	= 20 # Between 0 and 255, if used with something like 600 leds, have the brightness no more than ~75
LED_INVERT	= False

UPDATE_INTERVAL = 0.5 # how frequently to read the file and check for updates to the color data
FILE_PATH = "web/colorData"

colors = [0 for c in range(LED_COUNT)]
#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

# an object that will run in an infinite loop, drawing each time
# drawing 600 leds takes about ~0.02 seconds, or 50fps
class drawThread(object):
	def __init__(self, interval=0):
		self.interval = interval
		self.canRun = True
		thread = threading.Thread(target=self.run, args=())
		thread.name = "Draw Thread"
		thread.daemon = True
		thread.start()
	def run(self):
		try:
			while self.run:
				for x in range (LED_COUNT):
					try:
						if(colors[x] >= 0 and colors[x] <= (255 << 16 | 255 << 8 | 255)):
							strip.setPixelColor(x, colors[x])
					except OverflowError:
						print "color overflow"
				strip.show()
				time.sleep(self.interval)
		except:
			print "End of Draw Thread"

# returns the 24 bit color value based off of 3 byte values for rgb
def RGB(r, g, b):
	r = clamp(r)
	g = clamp(g)
	b = clamp(b)
	return (int(r) << 16) | (int(g) << 8) | int(b)

# returns the 24 bit color value based off of a tuple of (r, g, b) byte values
def RGBTuple(tuple):
	return RGB(tuple[0] * 255, tuple[1] * 255, tuple[2] * 255)

# returns the r value from a 24 bit color value
def getR(value):
	return value >> 16
# returns the g value from a 24 bit color value
def getG(value):
	return (value ^ (getR(value) << 16)) >> 8			
# returns the b value from a 24 bit color value
def getB(value):
	return (value ^ (getG(value) << 8))
# returns the value of n if it is within the bounds of smallest to largest, otherwise returns the
# smallest or largest value
def clamp(n, smallest = 0, largest = 255):
	return max(smallest, min(n, largest))
# makes a color wipe up from the bottom, with length speed seconds
def wipeUp(color, speed = 5):
	for x in range (LED_COUNT - 1):
		colors[x] = color
		time.sleep(float(speed / float(LED_COUNT)))
	return
# color wipe from the top, length speed seconds
def wipeDown(color, speed = 5):
	for x in range(LED_COUNT):
		colors[LED_COUNT - 1 - x] = color
		time.sleep(float(speed / float(LED_COUNT)))
	return

def setAllColor(color):
	colors = [color for c in range(LED_COUNT)]	

def setAllColorTuple(colorTuple):
	for x in range(LED_COUNT):
		colors[x] = RGBTuple(colorTuple)

# clears all of the color values and turns off the led strip
def cleanup():
	while (threading.active_count() > 2):
		# one thread is drawing, one is main thread
		print "Waiting for threads(" + str(threading.active_count() - 2) + ") to finish..."
		time.sleep(1)
	time.sleep(0.02)
	for c in range (strip.numPixels()):
		colors[c] = 0
		strip.setPixelColorRGB(c, 0,0,0)
	strip.show()

def randomBlinker(amount = 60, delay = 0.02, colorForeground = RGB(255, 255, 255), colorBackground = RGB(0,0,0)):
	#setAllColor(colorBackground)
	for led in range(amount):
		num = int(random.random() * 600)
		colors[num] = colorForeground
	time.sleep(delay)

# value is between 0 and 1, 0 is color1, 1 is color2, between that is a blend between them
def blendColor(value, color1_tuple, color2_tuple):
	valueInvert = abs(1 - value)
	return RGBTuple(color1_tuple[0] * value + color2_tuple[0] * valueInvert, color1_tuple[1] * value + color2_tuple[1] * valueInvert, color1_tuple[2] * value + color2_tuple[2] * valueInvert)

threads = []
def makeThread(Target, Args):
	t = threading.Thread(target=Target, args=Args)
	threads.append(t)
	t.start()

if __name__ == "__main__":
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	# start drawing thread
	drawTh = drawThread()
	print "Press Ctrl-C to quit"
	try:
		while True:
			red = 0
			green = 0
			blue = 0
			with open(FILE_PATH, "rb") as f:
				data = f.read(3)
				f.close()
				red = int(data[0].encode('hex'), 16)
				green = int(data[1].encode('hex'), 16)
				blue = int(data[2].encode('hex'), 16)
				color = RGB(red,green,blue)
				for x in range (LED_COUNT):
					colors[x] = color
			time.sleep(UPDATE_INTERVAL)

	except (KeyboardInterrupt, SystemExit):
		print "End of program"
		drawTh.canRun = False		
		cleanup()
