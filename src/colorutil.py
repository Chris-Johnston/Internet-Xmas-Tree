"""
Color Utility

Provides some utility functions for manipulating (r, g, b) colors.

Requires the pip package colorsys
"""

import colorsys

def rgbToTuple(r, g, b):
    r = clampColor(r)
    g = clampColor(g)
    b = clampColor(b)
    return (r, g, b)

def clampColor(val):
    return max(0, min(val, 255))

def getRGBFrom24Bit(value24Bit):
    return rgbToTuple(getRComponent(value24Bit), getGComponent(value24Bit), getBComponent(value24Bit))

def getColorFromString(str):
    return getRGBFrom24Bit(int(str,16))

# get the 24 bit color value based on 3 byte values for rgb
def get24BitColorValueRGB(r, g, b):
    r = clampColor(r)
    g = clampColor(g)
    b = clampColor(b)
    return (int(r) << 16) | (int(g) << 8) | int( b)

def get24BitColorValueArray(tupleRGB):
    return get24BitColorValueRGB(tupleRGB[0], tupleRGB[1], tupleRGB[2])

# get components from a 24 bit value

def getRComponent(value):
    return value >> 16

def getGComponent(value):
    return (value ^ (getRComponent(value) << 16)) >> 8

def getBComponent(value):
    return (value ^ (value >> 8) << 8)

# gets rgb tuple from hsv valus
def hsv(hue, saturation, value):
    return multiplyArray(colorsys.hsv_to_rgb(hue, saturation, value), 255)

# scale the color by this amt, useful for sin
def multiplyArray(value, scale):
    return ( clampColor(value[0] * scale), clampColor(value[1] * scale), clampColor(value[2] * scale))

def multiplyRGB(r, g, b, scale):
    return multiply(rtbToTuple(r,g,b), scale)

# fades the value to black
def toBlackArray(value, amtToReduce):
    return ( clampColor(value[0] - amtToReduce), clampColor(value[1] - amtToReduce), clampColor(value[2] - amtToReduce))

def toBlackRGB(r, g, b, amtToReduce):
    return toBlack(rgbToTuple(r,g,b), amtToReduce)

# combine values and clamp them
def addRGB(r, g, b, r2, g2, b2):
    return rgbToTuple(r + r2, g + g2, b + b2)

def addArray(tuple1, tuple2):
    return rgbToTuple(tuple1[0] + tuple2[0], tuple1[1] + tuple2[1], tuple1[2] + tuple2[2])
