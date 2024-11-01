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
        self.food_flash_counter: int = 0

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
            time.sleep(0.00001)
            GPIO.output(self.SRCLK, GPIO.LOW)

    def update_matrix(self, snake, food):
        self.food_flash_counter = (self.food_flash_counter + 1) % 20
        flash_food = self.food_flash_counter < 10

        for row in range(MATRIX_SIZE):
            row_data = 0
            for x in range(MATRIX_SIZE):
                if (x, row) in snake:
                    row_data |= (1 << x)
                elif (x, row) == food and flash_food:
                    row_data |= (1 << x)

            GPIO.output(self.RCLK, GPIO.LOW)
            self.shift_out(~row_data)
            self.shift_out(1 << row)
            GPIO.output(self.RCLK, GPIO.HIGH)

    def clear_matrix(self):
        GPIO.output(self.RCLK, GPIO.LOW)
        for _ in range(MATRIX_SIZE):
            self.shift_out(0xFF)
            self.shift_out(0)
        GPIO.output(self.RCLK, GPIO.HIGH)

    def cleanup(self):
        self.clear_matrix()
        GPIO.cleanup()

