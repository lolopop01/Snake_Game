#!/usr/bin/env python3

import wiimote
import sys

class WiiRemoteHandler:
    def __init__(self):
        self.wm = None
        self.connect()

    def connect(self):
        input("Press the 'sync' button on the back of your Wiimote Plus " +
              "or buttons (1) and (2) on your classic Wiimote.\n" +
              "Press <return> once the Wiimote's LEDs start blinking.")

        if len(sys.argv) == 1:
            addr, name = wiimote.find()[0]
        elif len(sys.argv) == 2:
            addr = sys.argv[1]
            name = None
        elif len(sys.argv) == 3:
            addr, name = sys.argv[1:3]
        print(("Connecting to %s (%s)" % (name, addr)))
        self.wm = wiimote.connect(addr, name)

def get_direction(self):
    directions = {
        "UP": [0, 0, 100],   # UP
        "DOWN": [0, 0, -100],   # DOWN
        "LEFT": [-100, 0, 0],  # LEFT
        "RIGHT": [100, 0, 0]     # RIGHT
    }

    accelerometer_data = self.wm.accelerometer
    closest_direction = None
    max_strength = 0  # To keep track of the strongest direction match

    # Define tolerance levels (the difference between the axes we accept)
    tolerance = 30  # This is the acceptable margin for the direction comparison

    for direction, reference in directions.items():
        # Check if the corresponding axis is dominant
        if direction == "UP" or direction == "DOWN":
            # Check if the Z axis is dominant (up or down)
            if abs(accelerometer_data[2]) - abs(accelerometer_data[0]) > tolerance and abs(accelerometer_data[2]) - abs(accelerometer_data[1]) > tolerance:
                strength = abs(accelerometer_data[2])  # The dominant axis (Z) strength
                if strength > max_strength:
                    max_strength = strength
                    closest_direction = direction
        elif direction == "LEFT" or direction == "RIGHT":
            # Check if the X axis is dominant (left or right)
            if abs(accelerometer_data[0]) - abs(accelerometer_data[1]) > tolerance and abs(accelerometer_data[0]) - abs(accelerometer_data[2]) > tolerance:
                strength = abs(accelerometer_data[0])  # The dominant axis (X) strength
                if strength > max_strength:
                    max_strength = strength
                    closest_direction = direction

    return closest_direction
