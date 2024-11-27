#!/usr/bin/env python3
import threading

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

    def get_direction(self, old_direction):
        directions = {
            (0, -1): [0, 0, 100],   # UP
            (0, 1): [0, 0, -100],   # DOWN
            (-1, 0): [-100, 0, 0],  # LEFT
            (1, 0): [100, 0, 0],     # RIGHT
            None : [0, 0, 0] # DEFAULT
        }

        accelerometer_data = self.wm.accelerometer
        closest_direction = (0, 0)
        smallest_distance = float('inf')

        for direction, reference in directions.items():
            distance = sum((accelerometer_data[i] - reference[i]) ** 2 for i in range(3))
            if distance < smallest_distance:
                smallest_distance = distance
                closest_direction = direction

        # if closest_direction and tuple(-x for x in old_direction) == closest_direction:
            # return old_direction

        return closest_direction

    def play_eat_sound(self):
        sound_thread = threading.Thread(target=self.play_custom_sound_in_thread, args=("./Sounds/Eat_4bit_3000Hz.wav",))
        sound_thread.start()

    def play_custom_sound_in_thread(self, file_path):
        self.wm.speaker.play_custom_sound(file_path)

