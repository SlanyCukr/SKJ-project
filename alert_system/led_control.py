import time
import random

from rpi_ws281x import *


def get_strip() -> Adafruit_NeoPixel:
    """
    Gets LED strip.
    """
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    return strip


def generate_pretty_color():
    colors = [random.randint(128, 255), random.randint(0,50), random.randint(0, 25)]

    red_index = random.randint(0, 2)
    color_red = colors[red_index]
    del colors[red_index]

    green_index = random.randint(0, 1)
    color_green = colors[green_index]

    color_blue = colors[green_index - 1]
    return color_red, color_green, color_blue


# LED strip configuration:
LED_COUNT = 178      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
RANDOM_COLOR_TTL = 100

strip = get_strip()
random_color_timer = 0

random_color_red, random_color_green, random_color_blue = generate_pretty_color()

random_dest_color_red, random_dest_color_green, random_dest_color_blue = generate_pretty_color()


def flash():
    color = generate_pretty_color()
    for i in range(10):
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, color)
        strip.show()
        time.sleep(0.25)
