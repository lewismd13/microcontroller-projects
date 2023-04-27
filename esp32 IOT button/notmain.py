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
    print(
        "\t%s\t\tRSSI: %d\tChannel: %d"
        % (str(network.ssid, "utf-8"), network.rssi, network.channel)
    )
wifi.radio.stop_scanning_networks()


def connect_attempt():
    try:
        wifi.radio.connect(secrets["ssid"], secrets["password"])
    except Exception:
        time.sleep(300)
        wifi.radio.connect(secrets["ssid"], secrets["password"])


print("Connecting to %s" % secrets["ssid"])
connect_attempt()
print("Connected to %s!" % secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4) * 1000))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

print("done")

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixels[0] = (10, 10, 0)

button = digitalio.DigitalInOut(board.A0)

OUTLET_URL = "http://192.168.86.42/cm?cmnd=Power%20TOGGLE"

while True:
    print(button.value)
    if not button.value:
        pixels[0] = (255, 0, 0)
        time.sleep(0.2)
        try:
            response = requests.get(OUTLET_URL)
        except:
            wifi.radio.connect(secrets["ssid"], secrets["password"])
            response = requests.get(OUTLET_URL)
        pixels[0] = (0, 0, 0)
    else:
        # r_value = random.randint(0, 255)
        # g_value = random.randint(0, 255)
        # b_value = random.randint(0, 255)
        # pixels[0] = (r_value, g_value, b_value)
        time.sleep(0.2)
