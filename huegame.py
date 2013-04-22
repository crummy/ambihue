__author__ = 'Malcolm'
import time
import sys
from phue import Bridge
from PIL import ImageGrab


def getAverageScreenColor():
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


# From:
#https://github.com/PhilipsHue/PhilipsHueSDKiOS/blob/master/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md
def rgbToXy(r, g, b):
    r = pow((r + 0.055) / (1.0 + 0.055), 2.4) if r > 0.04045 else r / 12.92
    g = pow((g + 0.055) / (1.0 + 0.055), 2.4) if g > 0.04045 else g / 12.92
    b = pow((b + 0.055) / (1.0 + 0.055), 2.4) if b > 0.04045 else b / 12.92
    X = r * 0.649926 + g * 0.103455 + b * 0.197109
    Y = r * 0.234327 + g * 0.743075 + b * 0.022598
    Z = r * 0.000000 + g * 0.053077 + b * 1.035763
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    print "rgb returns x: %s and y: %s" % (x, y)
    return x, y


def turnLightToColor(bridge, light, red, green, blue):
    print "red: %s, green: %s, blue: %s" % (red, green, blue)
    x, y = rgbToXy(red/255, green/255, blue/255)
    #x = int(x * 360*182)
    #y = int(y * 255)
    light = bridge.get_light_objects('id')
    light[2].xy = (x, y)

if len(sys.argv) < 2:
    print "Game Hue needs a better name, by Malcolm Crum"
    print "Usage: python huegame.py <huehubIP>"
else:
    hueIP = sys.argv[1]
    bridge = Bridge(hueIP)
    start_time = time.time()
    interval = 0.5
    i = 0
    while True:
        time.sleep(start_time + i * interval - time.time())
        i += 1
        r, g, b = getAverageScreenColor()
        turnLightToColor(bridge, 2, r, g, b)
