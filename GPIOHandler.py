import RPi.GPIO as GPIO
import time

# GPIO Pins for Shift Registers
SDI = 17   # Serial data input
RCLK = 18  # Latch pin
SRCLK = 27 # Clock pin

# Matrix Size (8x8)
MATRIX_SIZE = 8


class GPIOHandler:
    def __init__(self):
        self.SDI = SDI
        self.RCLK = RCLK
        self.SRCLK = SRCLK

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SDI, GPIO.OUT)
        GPIO.setup(self.RCLK, GPIO.OUT)
        GPIO.setup(self.SRCLK, GPIO.OUT)

        GPIO.output(self.SDI, GPIO.LOW)
        GPIO.output(self.RCLK, GPIO.LOW)
        GPIO.output(self.SRCLK, GPIO.LOW)

    def shift_out(self, data):
        # Shift out 8 bits of data to the shift registers
        for bit in range(8):
            GPIO.output(self.SDI, (data >> (7 - bit)) & 1)
            GPIO.output(self.SRCLK, GPIO.HIGH)
            time.sleep(0.00000001)
            GPIO.output(self.SRCLK, GPIO.LOW)

    def update_matrix(self, snake, food):
        for row in range(MATRIX_SIZE):
            row_data = 0
            for x in range(MATRIX_SIZE):
                if (x, row) in snake:
                    row_data |= (1 << x)
                elif (x, row) == food:
                    row_data |= (1 << x)  # Handle food separately if needed

            # Send data to the shift registers
            GPIO.output(self.RCLK, GPIO.LOW)
            self.shift_out(~row_data)
            self.shift_out(1 << row)
            GPIO.output(self.RCLK, GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup()
