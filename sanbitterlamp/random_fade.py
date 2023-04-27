import neopixel
import board
import time
import random

red = 0
green = 0
blue = 0


pixel_pin = board.GP20
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(
    pixel_pin, 1, brightness=0.8, auto_write=False, pixel_order=ORDER
)

pixels.fill(red, green, blue)
pixels.show()

while True:
    red_target = random.randint(0, 255)
    green_target = random.randint(0, 255)
    blue_target = random.randint(0, 255)

    while red != red_target and green != green_target and blue != blue_target:
        if red > red_target:
            red = red - 1
        elif red < red_target:
            red = red + 1
        if green > green_target:
            green = green - 1
        elif green < green_target:
            green = green + 1
        if blue > blue_target:
            blue = blue - 1
        elif blue < blue_target:
            blue = blue + 1
        pixels.fill(red, green, blue)
        pixels.show()
        time.sleep(1)
