import RPi.GPIO as GPIO
import time
import random

# GPIO Pins for Shift Registers
SDI = 17   # Serial data input
RCLK = 18  # Latch pin
SRCLK = 27 # Clock pin

# GPIO Button Pins for Direction Control
UP_PIN = 5
DOWN_PIN = 6
LEFT_PIN = 13
RIGHT_PIN = 19

# Game Configuration
MATRIX_SIZE = 8

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        # Initial state of the game
        self.snake = [(3, 3)]  # Initial position of the snake
        self.food = self.generate_food()
        self.direction = RIGHT

        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SDI, GPIO.OUT)
        GPIO.setup(RCLK, GPIO.OUT)
        GPIO.setup(SRCLK, GPIO.OUT)
        GPIO.output(SDI, GPIO.LOW)
        GPIO.output(RCLK, GPIO.LOW)
        GPIO.output(SRCLK, GPIO.LOW)

        GPIO.setup(UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Register button press callbacks
        GPIO.add_event_detect(UP_PIN, GPIO.FALLING, callback=self.change_direction, bouncetime=200)
        GPIO.add_event_detect(DOWN_PIN, GPIO.FALLING, callback=self.change_direction, bouncetime=200)
        GPIO.add_event_detect(LEFT_PIN, GPIO.FALLING, callback=self.change_direction, bouncetime=200)
        GPIO.add_event_detect(RIGHT_PIN, GPIO.FALLING, callback=self.change_direction, bouncetime=200)

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

    def update_matrix(self):
        # Create an 8x8 matrix representation
        matrix = [0] * MATRIX_SIZE
        for x, y in self.snake:
            matrix[y] |= (1 << x)
        matrix[self.food[1]] |= (1 << self.food[0])

        # Send data to the shift registers
        GPIO.output(RCLK, GPIO.LOW)
        for row in matrix:
            self.shift_out(~row)  # Active LOW, invert bits
            self.shift_out(1 << matrix.index(row))
        GPIO.output(RCLK, GPIO.HIGH)

    def change_direction(self, channel):
        if channel == UP_PIN and self.direction != DOWN:
            self.direction = UP
        elif channel == DOWN_PIN and self.direction != UP:
            self.direction = DOWN
        elif channel == LEFT_PIN and self.direction != RIGHT:
            self.direction = LEFT
        elif channel == RIGHT_PIN and self.direction != LEFT:
            self.direction = RIGHT

    def move_snake(self):
        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        # Check for collisions with walls or itself
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= MATRIX_SIZE or
            new_head[1] < 0 or new_head[1] >= MATRIX_SIZE):
            print("Game Over!")
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
            while True:
                self.move_snake()
                self.update_matrix()
                time.sleep(0.5)  # Adjust speed as needed
        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
