# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

"""create the trellis. This is for a 2x2 array of NeoTrellis boards
for a 2x1 array (2 boards connected left to right) you would use:

trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x2F)]
    ]

"""
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x2F)],
    [NeoTrellis(i2c_bus, False, addr=0x30), NeoTrellis(i2c_bus, False, addr=0x31)],
]

trellis = MultiTrellis(trelli)
tempo = 240  # Starting BPM

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 24)
PURPLE = (12, 0, 24)
ACTIVE_COLOR = PURPLE
INACTIVE_COLOR = BLUE
CURRENT_COLOR = INACTIVE_COLOR
HEIGHT = 8
WIDTH = 8
CURRENT_STEP = 0
ACTIVE_KEYS = []
key_list=[]
for x in range(WIDTH):
    for y in range(HEIGHT):
        key_list.append([x,y])
# this will be called when button events are received
def blink(xcoord, ycoord, edge):
    # turn the LED on when a rising edge is detected
    if edge == NeoTrellis.EDGE_RISING:
        trellis.color(xcoord, ycoord, ACTIVE_COLOR)
        position=(xcoord, ycoord)
        print(position)
        if position in ACTIVE_KEYS:
            ACTIVE_KEYS.remove(position)
        else:
            ACTIVE_KEYS.append(position)
        print(ACTIVE_KEYS)
    # turn the LED off when a rising edge is detected

    for i in ACTIVE_KEYS:
        trellis.color(i[0], i[1], ACTIVE_COLOR)


# startup pattern
for y in range(8):
    for x in range(8):
        # activate rising edge events on all keys
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        # activate falling edge events on all keys
        trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
        trellis.set_callback(x, y, blink)
        trellis.color(x, y, ACTIVE_COLOR)
        time.sleep(0.01)
for y in range(8):
    for x in range(8):
        trellis.color(x, y, INACTIVE_COLOR)
        time.sleep(0.01)

while True:
    # the trellis can only be read every 17 millisecons or so
    if CURRENT_STEP < 7:
        CURRENT_STEP+=1

    else:
        CURRENT_STEP = 0

    if CURRENT_STEP == 0:
        PREVIOUS_STEP = 7
    else:
        PREVIOUS_STEP = CURRENT_STEP -1

    for row in range(HEIGHT-6, HEIGHT):
        trellis.color(CURRENT_STEP, row, ACTIVE_COLOR)
        if (PREVIOUS_STEP, row) not in ACTIVE_KEYS:
            print(PREVIOUS_STEP, ACTIVE_KEYS)
            trellis.color(PREVIOUS_STEP, row, INACTIVE_COLOR)



    stamp = time.monotonic()
    # handle button presses while we're waiting for the next tempo beat
    while time.monotonic() - stamp < 60/tempo:
        trellis.sync()
        time.sleep(0.02)  # a little delay here helps avoid debounce annoyances