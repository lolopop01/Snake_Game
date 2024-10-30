from GPIOHandler import *
import time
import random
import keyboard
import threading
import os

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game Configuration
MATRIX_SIZE = 8
MOVE_INTERVAL = 0.5  # Time in seconds between moves

class SnakeGame:
    def __init__(self):
        self.snake = [(3, 3), (3, 2), (3, 1)]  # Initial position of the snake (length 3)
        self.food = self.generate_food()
        self.direction = RIGHT
        self.running = True

        self.gpio_handler = GPIOHandler()

        # Start the input thread
        self.input_thread = threading.Thread(target=self.change_direction)
        self.input_thread.start()

        # Start the display thread
        self.display_thread = threading.Thread(target=self.update_display)
        self.display_thread.start()

        # Start the display console thread
        self.display_console_thread = threading.Thread(target=self.display_matrix)
        self.display_console_thread.start()

    def end(self):
        self.running = False
        self.display_console_thread.join()
        self.display_thread.join()
        self.input_thread.join()
        self.gpio_handler.cleanup()
        exit()

    def generate_food(self):
        while True:
            food = (random.randint(0, MATRIX_SIZE - 1), random.randint(0, MATRIX_SIZE - 1))
            if food not in self.snake:
                return food

    def display_matrix(self):
        while self.running:
            time.sleep(0.1)
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

    def update_display(self):
        while self.running:
            self.gpio_handler.update_matrix(self.snake, self.food)

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
            self.end()

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
            self.end()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
