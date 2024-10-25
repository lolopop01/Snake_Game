import RPi.GPIO as GPIO
import time
import random
import threading
import os
import sys
import tty
import termios

SDI = 17
RCLK = 18
SRCLK = 27

MATRIX_SIZE = 8
MOVE_INTERVAL = 0.5

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.snake = [(3, 3), (3, 2), (3, 1)]
        self.food = self.generate_food()
        self.direction = RIGHT
        self.running = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SDI, GPIO.OUT)
        GPIO.setup(RCLK, GPIO.OUT)
        GPIO.setup(SRCLK, GPIO.OUT)

        self.input_thread = threading.Thread(target=self.change_direction)
        self.input_thread.start()

        self.display_thread = threading.Thread(target=self.update_matrix)
        self.display_thread.start()

        self.display_console_thread = threading.Thread(target=self.display_matrix)
        self.display_console_thread.start()

    def generate_food(self):
        while True:
            food = (random.randint(0, MATRIX_SIZE - 1), random.randint(0, MATRIX_SIZE - 1))
            if food not in self.snake:
                return food

    def shift_out(self, data):
        for bit in range(8):
            GPIO.output(SDI, (data >> (7 - bit)) & 1)
            GPIO.output(SRCLK, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(SRCLK, GPIO.LOW)

    def display_matrix(self):
        while self.running:
            os.system('clear')
            for y in range(MATRIX_SIZE):
                row = ""
                for x in range(MATRIX_SIZE):
                    if (x, y) in self.snake:
                        row += "S"
                    elif (x, y) == self.food:
                        row += "F"
                    else:
                        row += "."
                print(row)
            time.sleep(0.1)

    def update_matrix(self):
        while self.running:
            GPIO.output(RCLK, GPIO.LOW)
            for row in range(MATRIX_SIZE):
                row_data = 0
                for x in range(MATRIX_SIZE):
                    if (x, row) in self.snake:
                        row_data |= (1 << x)
                    elif (x, row) == self.food:
                        row_data |= (1 << x)
                self.shift_out(~row_data)
                self.shift_out(1 << row)
            GPIO.output(RCLK, GPIO.HIGH)
            time.sleep(0.001)

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

    def change_direction(self):
        while self.running:
            key = self.get_key()
            if key == 'w' and self.direction != DOWN:
                self.direction = UP
            elif key == 's' and self.direction != UP:
                self.direction = DOWN
            elif key == 'a' and self.direction != RIGHT:
                self.direction = LEFT
            elif key == 'd' and self.direction != LEFT:
                self.direction = RIGHT
            time.sleep(0.1)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= MATRIX_SIZE or
            new_head[1] < 0 or new_head[1] >= MATRIX_SIZE):
            print("Game Over!")
            self.running = False
            GPIO.cleanup()
            exit()

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def run(self):
        try:
            while self.running:
                self.move_snake()
                time.sleep(MOVE_INTERVAL)
        except KeyboardInterrupt:
            self.running = False
            GPIO.cleanup()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
