# xmasWeb.py
from Configuration import Configuration

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

UPDATE_INTERVAL = 0.0 # how frequently to read the file and check for updates to the color data
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
	return RGB(tuple[0], tuple[1], tuple[2])

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
	for x in range (LED_COUNT):
		colors[x] = RGBTuple(color)
		time.sleep(float(speed / float(LED_COUNT)))
# color wipe from the top, length speed seconds
def wipeDown(color, speed = 5):
	for x in range(LED_COUNT):
		colors[LED_COUNT - 1 - x] = RGBTuple(color)
		time.sleep(float(speed / float(LED_COUNT)))

# a "larson scanner" styled pattern	
def larsonScanner(width = 5, speed = 4, colorForeground = RGB(255, 0,0), colorBackground = RGB(0,0,0)):
	# first wipe up
	for x in range(int(LED_COUNT - width)):
		setAllColorTuple(colorBackground)
		for i in range(int(width)):
			colors[x + i] = RGBTuple(colorForeground)
		time.sleep(float((speed / 2.0) / (LED_COUNT - width)))
	# then wipe down
	for x in range(int(LED_COUNT - width)):
		setAllColorTuple(colorBackground)
		for i in range(int(width)):
			colors[LED_COUNT - 1 - x + i] = RGBTuple(colorForeground)
		time.sleep(float((speed / 2.0) / (LED_COUNT - width)))

def setAllColor(color):
	#colors = [color for c in range(LED_COUNT)]	
	for x in range(LED_COUNT):
		colors[x] = color

def setAllColorTuple(colorTuple):
	setAllColor(RGBTuple(colorTuple))
	#for x in range(LED_COUNT):
	#	colors[x] = RGBTuple(colorTuple)

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
	setAllColorTuple(colorBackground)
	for led in range(int(amount)):
		num = int(random.random() * 600)
		colors[num] = RGBTuple(colorForeground)
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

tc = 0
def twoColorScroll(color1, color2, width, delay):
	global tc
	tc = tc + 1
	if(tc > 2 * width - 1):
		tc = 0
	for led in range (LED_COUNT):
		if(int((tc + led) / width % 2) == 1):
			colors[led] = RGBTuple(color1)
		else:
			colors[led] = RGBTuple(color2)
	time.sleep(delay / 1000.0 + UPDATE_INTERVAL)

def getRandomColor():
	return (255 * random.random(), 255 * random.random(), 255 * random.random())

if __name__ == "__main__":
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	# start drawing thread
	drawTh = drawThread()
	color1 = (0,0,0)
	twoColorScrollCounter = 0
	color2 = (0,0,0)
	pattern = 0
	random1 = 0
	random2 = 0
	length = 0
	delay = 0
	print "Press Ctrl-C to quit"
	try:
		while True:
			# R, G, B Color 1 Bytes, R, G, B Color 2 Bytes, Random Flag 1, Random Flag 2, Pattern Byte, 
			# Length Value 
			# Delay Value
			with open(FILE_PATH, "rb") as f:
				dataBytes = f.readline()
				try:
					length = float(f.readline())
				except ValueError:
					length = 15
				try:
					delay = float(f.readline())
				except ValueError:
					delay = 100
				f.close()
				
				r = int(dataBytes[0].encode('hex'), 16)
				g = int(dataBytes[1].encode('hex'), 16)
				b = int(dataBytes[2].encode('hex'), 16)
				
				color1 = (r, g, b)

				r = int(dataBytes[3].encode('hex'), 16)
				g = int(dataBytes[4].encode('hex'), 16)
				b = int(dataBytes[5].encode('hex'), 16)
				
				color2 = (r, g, b)

				random1 = int(dataBytes[6].encode('hex'), 16)
				random2 = int(dataBytes[7].encode('hex'), 16)
				
				pattern = int(dataBytes[8].encode('hex'), 16)

			#print ""
			#print color1
			#print color2
			#print (pattern, length, delay)

			if(random1 == 1):
				#print "rand 1"
				color1 = getRandomColor()
			if(random2 == 1):
				#print "rand 2"
				color2 = getRandomColor()

			if(pattern == 0):
				# solid color
				setAllColorTuple(color1)
				#print "solid color ", color1
			elif(pattern == 1):
				#blink colors
				setAllColorTuple(color1)
				#print "color1"
				time.sleep(UPDATE_INTERVAL + delay / 1000.0)
				setAllColorTuple(color2)
				#print "color2"
			elif(pattern == 2):
				# Scroll Colors
				#print "2 color scroll"
				twoColorScroll(color1, color2, length, delay)
			elif(pattern == 3):
				# wipe up
				wipeUp(color1, delay / 1000.0)
				#print "wipe c1"
				time.sleep(UPDATE_INTERVAL + delay / 1000.0)
				#print "wipe c2"
				wipeUp(color2, delay / 1000.0)
			elif(pattern == 4):
				# wipe down
				#print "wipe c1"
				wipeDown(color1, delay / 1000.0)
				time.sleep(UPDATE_INTERVAL + delay / 1000.0)
				#print "wipe c2"
				wipeDown(color2, delay / 1000.0)
			elif(pattern == 6):
				# larson scanner
				larsonScanner(length, delay, color1, color2)
			elif(pattern == 5):
				t = time.time()
				#print "blinker"
				while (time.time() - t < 5):
					randomBlinker(length, delay / 1000.0, color1, color2)
			if(pattern != 5):
				# random blinker works differently, and to prevent it from constantly reading over
				# and over again, only have it update every now and then
				time.sleep(UPDATE_INTERVAL + delay / 1000.0)
	except (KeyboardInterrupt, SystemExit):
		print "End of program"
		drawTh.canRun = False		
		cleanup()
