# color utilities
import colorsys

def rgbToTuple(r, g, b):
    return (r, g, b)

def clampColor(val):
    return max(0, min(val, 255))

def getRGBFrom24Bit(value24Bit):
    return rgbToTuple(getRComponent(value24Bit), getGComponent(value24Bit), getBComponent(value24Bit))

def getColorFromString(str):
    return getRGBFrom24Bit(int(str, 16))

# get the 24 bit color value based on 3 byte values for rgb
def get24BitColorValue(r, g, b):
    r = clampColor(r)
    g = clampColor(g)
    b = clampColor(b)
    return (int(r) << 16) | (int(g) << 8) | int(b)

def get24BitColorValue(tupleRGB):
    return get24BitColorValue(tupleRGB[0], tupleRGB[1], tupleRGB[2])

# get components from a 24 bit value

def getRComponent(value):
    return value >> 16

def getGComponent(value):
    return (value ^ (getR(value) << 16)) >> 8

def getBComponent(value):
    return (value ^ (getG(value) << 8))

# gets rgb tuple from hsv valus
def hsv(hue, saturation, value):
    return colorsys.hsv_to_rgb(hue, saturation, value)

# scale the color by this amt, useful for sin
def multiply(value, scale):
    return ( clampColor(value[0] * scale), clampColor(value[1] * scale), clampColor(value[2] * scale))

def multiply(r, g, b, scale):
    return multiply(rtbToTuple(r,g,b), scale)

# fades the value to black
def toBlack(value, amtToReduce):
    return ( clampColor(value[0] - amtToReduce), clampColor(value[1] - amtToReduce), clampColor(value[2] - amtToReduce))

def toBlack(r, g, b, amtToReduce):
    return toBlack(rgbToTuple(r,g,b), amtToReduce)

# combine values and clamp them
def add(r, g, b, r2, g2, b2):
    return rgbToTuple(r + r2, g + g2, b + b2)

def add(tuple1, tuple2):
    return rgbToTuple(tuple1[0] + tuple2[0], tuple1[1] + tuple2[1], tuple1[2] + tuple2[2])