#!/usr/bin/env python
""" Ambient Hue Lighting Controller
    Regularly sets a Phillips Hue light to the average screen colour
"""
import time
import sys
from phue import Bridge
from PIL import ImageGrab

__author__ = "Malcolm Crum"
__license__ = "WTFPL"
__version__ = "0.1"
__email__ = "crummynz@gmail.com"
__status__ = "Proof of concept"


def getAverageScreenColor():
    """ Examines 1/64th the pixels on the screen, calculates the average colour, and returns
        the average in the form of three floats.
    """
    screen = ImageGrab.grab()
    left, top, width, height = screen.getbbox()
    red, green, blue = 0.0, 0.0, 0.0
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            color = screen.getpixel((x, y))
            red += color[0]
            green += color[1]
            blue += color[2]
    total = y/8 * x/8
    red /= total
    blue /= total
    green /= total
    return red, green, blue


def rgbToXy(r, g, b):
    """ Calculates the XY values (in the Hue's colourspace) from given RGB values.
        Uses formula from https://github.com/PhilipsHue/PhilipsHueSDKiOS/blob/master/ApplicationDesignNotes/
                                                                        RGB%20to%20xy%20Color%20conversion.md
        Returns two floats; the X and Y values of the colour.
    """
    r = pow((r + 0.055) / (1.0 + 0.055), 2.4) if r > 0.04045 else r / 12.92
    g = pow((g + 0.055) / (1.0 + 0.055), 2.4) if g > 0.04045 else g / 12.92
    b = pow((b + 0.055) / (1.0 + 0.055), 2.4) if b > 0.04045 else b / 12.92
    X = r * 0.649926 + g * 0.103455 + b * 0.197109
    Y = r * 0.234327 + g * 0.743075 + b * 0.022598
    Z = r * 0.000000 + g * 0.053077 + b * 1.035763
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    #print "rgb returns x: %s and y: %s" % (x, y)
    return x, y


def turnLightToColor(bridge, id, red, green, blue):
    """ Given a bridge, light ID, and colour, sets the given light to the colour specified.
    """
    #print "red: %s, green: %s, blue: %s" % (red, green, blue)
    x, y = rgbToXy(red/255, green/255, blue/255)
    bri = int((red + green + blue)/3)
    command = {'transitiontime': 3, 'on': True, 'bri': bri, 'xy': (x, y)}
    bridge.set_light(id, command)


if len(sys.argv) < 2:
    print "Ambient Hue Lighting Controller, by Malcolm Crum"
    print "Usage: python huegame.py <huehubIP> <lightID>"
else:
    hueIP = sys.argv[1]
    light = sys.argv[2]
    bridge = Bridge(hueIP)
    start_time = time.time()
    interval = 0.2  # How many seconds to wait between screen refreshes
    i = 0
    while True:
        time.sleep(start_time + i * interval - time.time())
        i += 1
        r, g, b = getAverageScreenColor()
        turnLightToColor(bridge, int(light), r, g, b)
