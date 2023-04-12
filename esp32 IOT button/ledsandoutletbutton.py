# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import neopixel
import time
import digitalio
import random

# URLs to fetch from
TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_QUOTES_URL = "https://www.adafruit.com/api/quotes.php"
JSON_STARS_URL = "https://api.github.com/repos/adafruit/circuitpython"

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("ESP32-S2 WebClient Test")

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

print("Available WiFi networks:")
for network in wifi.radio.start_scanning_networks():
    print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
            network.rssi, network.channel))
wifi.radio.stop_scanning_networks()

print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

print("Fetching text from", TEXT_URL)
response = requests.get(TEXT_URL)
print("-" * 40)
print(response.text)
print("-" * 40)

print("Fetching json from", JSON_QUOTES_URL)
response = requests.get(JSON_QUOTES_URL)
print("-" * 40)
print(response.json())
print("-" * 40)

print()

print("Fetching and parsing json from", JSON_STARS_URL)
response = requests.get(JSON_STARS_URL)
print("-" * 40)
print("CircuitPython GitHub Stars", response.json()["stargazers_count"])
print("-" * 40)

print("done")

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=.1)
pixels[0] = (10, 10, 0)

button = digitalio.DigitalInOut(board.A0)

OUTLET_URL = "http://192.168.86.42/cm?cmnd=Power%20TOGGLE"

while True:
    print(button.value)
    if not button.value:
        pixels[0] = (255, 0, 0)
        time.sleep(.3)
        response = requests.get(OUTLET_URL)
    else:
        r_value = random.randint(0, 255)
        g_value = random.randint(0, 255)
        b_value = random.randint(0, 255)
        pixels[0] = (r_value, g_value, b_value)
        time.sleep(.3)

