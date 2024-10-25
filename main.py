import RPi.GPIO as GPIO
import time
import random
import keyboard  # Import the keyboard library
import threading
import os  # For clearing the terminal

# GPIO Pins for Shift Registers
SDI = 17   # Serial data input
RCLK = 18  # Latch pin
SRCLK = 27 # Clock pin

# Game Configuration
MATRIX_SIZE = 8
MOVE_INTERVAL = 0.5  # Time in seconds between moves

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        # Initial state of the game
        self.snake = [(3, 3), (3, 2), (3, 1)]  # Initial position of the snake (length 3)
        self.food = self.generate_food()
        self.direction = RIGHT
        self.running = True

        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SDI, GPIO.OUT)
        GPIO.setup(RCLK, GPIO.OUT)
        GPIO.setup(SRCLK, GPIO.OUT)
        GPIO.output(SDI, GPIO.LOW)
        GPIO.output(RCLK, GPIO.LOW)
        GPIO.output(SRCLK, GPIO.LOW)

        # Start the input thread
        self.input_thread = threading.Thread(target=self.change_direction)
        self.input_thread.start()

        # Start the display thread
        self.display_thread = threading.Thread(target=self.update_matrix)
        self.display_thread.start()

        # Start the display console thread
        self.display_console_thread = threading.Thread(target=self.display_matrix)

    def generate_food(self):
        while True:
            food = (random.randint(0, MATRIX_SIZE - 1), random.randint(0, MATRIX_SIZE - 1))
            if food not in self.snake:
                return food

    def shift_out(self, data):
        # Shift out 8 bits of data to the shift registers
        for bit in range(8):
            GPIO.output(SDI, (data >> (7 - bit)) & 1)
            GPIO.output(SRCLK, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(SRCLK, GPIO.LOW)

    # Display the matrix in the terminal
    def display_matrix(self):
        os.system('clear')  # Clear the terminal
        for y in range(MATRIX_SIZE):
            row = ""
            for x in range(MATRIX_SIZE):
                if (x, y) in self.snake:
                    row += "S"  # Snake segment
                elif (x, y) == self.food:
                    row += "F"  # Food
                else:
                    row += "."  # Empty space
            print(row)

    def update_matrix(self):
        # Send data to the shift registers (optional)
        GPIO.output(RCLK, GPIO.LOW)
        for row in range(MATRIX_SIZE):
            row_data = 0
            for x in range(MATRIX_SIZE):
                if (x, row) in self.snake:
                    row_data |= (1 << x)
                elif (x, row) == self.food:
                    row_data |= (1 << x)  # Could also handle food separately if needed
            self.shift_out(~row_data)  # Active LOW, invert bits
            self.shift_out(1 << row)  # Shift row indicator
        GPIO.output(RCLK, GPIO.HIGH)

    def change_direction(self):
        while self.running:
            if keyboard.is_pressed('up') and self.direction != DOWN:
                self.direction = UP
            elif keyboard.is_pressed('down') and self.direction != UP:
                self.direction = DOWN
            elif keyboard.is_pressed('left') and self.direction != RIGHT:
                self.direction = LEFT
            elif keyboard.is_pressed('right') and self.direction != LEFT:
                self.direction = RIGHT
            time.sleep(0.1)  # Short sleep to prevent busy waiting

    def move_snake(self):
        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        # Check for collisions with walls or itself
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= MATRIX_SIZE or
            new_head[1] < 0 or new_head[1] >= MATRIX_SIZE):
            print("Game Over!")
            self.running = False  # Stop the game loop
            GPIO.cleanup()
            exit()

        # Move the snake
        self.snake.insert(0, new_head)

        # Check if the snake eats the food
        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()  # Remove tail if no food is eaten

    def run(self):
        try:
            while self.running:
                self.move_snake()
                time.sleep(MOVE_INTERVAL)  # Wait for the specified move interval
        except KeyboardInterrupt:
            self.running = False
            GPIO.cleanup()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
