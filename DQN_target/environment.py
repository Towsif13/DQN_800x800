from collections import namedtuple
import pygame
import numpy as np

BLOCK_SIZE = 8
WIDTH = 800
HEIGHT = 800

# COLOR CODES
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREY = (224, 224, 224)


class Drone:
    def __init__(self, size, color):
        self.size = size
        self.color = color

    def place_drone(self, screen_width, screen_height):
        x = 0 + self.size + 0
        y = screen_height - self.size - 0

        return x, y

    def drone_move(self, x, y, move_distace, choice):
        if choice == 0:  # left
            x -= move_distace
        if choice == 1:  # right
            x += move_distace
        if choice == 2:  # up
            y += move_distace
        if choice == 3:  # down
            y -= move_distace

        return x, y


class Man:
    def __init__(self, size, color):
        self.size = size
        self.color = color

    def place_man(self, drone_x, drone_y, screen_width, screen_height):

        x = screen_width - self.size - 0
        y = 0 + self.size + 0

        return x, y

    # def place_man_2(self, drone_x, drone_y, screen_width, screen_height):
    #     x = screen_width - self.size - 0
    #     y = 0 + self.size + 60

    #     return x, y

    def move_man(self, man_x, man_y, pixel_per_step, direction):
        if direction == 'left':
            man_x -= pixel_per_step
        if direction == 'right':
            man_x += pixel_per_step
        if direction == 'down':
            man_y += pixel_per_step
        if direction == 'up':
            man_y -= pixel_per_step

        return man_x, man_y


class Environment:

    def __init__(self, w=WIDTH, h=HEIGHT):
        self.drone = Drone(BLOCK_SIZE, BLUE1)
        self.man = Man(BLOCK_SIZE, RED)
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode(
            (self.w, self.h))  # init display
        pygame.display.set_caption('BLOCK ENV')
        self.iteration = 0
        self.constant = 100
        self.alpha = 0.01
        self.reset()

    def reset(self):
        self.drone_x, self.drone_y = self.drone.place_drone(WIDTH, HEIGHT)

        self.man_x, self.man_y = self.man.place_man(
            self.drone_x, self.drone_y, WIDTH, HEIGHT)

        self.iteration = 0

        self.MAN_INITIAL_X, self.MAN_INITIAL_Y = self.man_x, self.man_y

        # return np.array([self.drone_x, self.drone_y, self.MAN_INITIAL_X, self.MAN_INITIAL_Y])
        return np.array([self.drone_x, self.drone_y])

    def is_drone_outside(self):
        if self.drone_x > self.w - BLOCK_SIZE or self.drone_x < 0 or self.drone_y > self.h - BLOCK_SIZE or self.drone_y < 0:
            return True
        return False

    def is_man_outside(self):
        if self.man_x > self.w - BLOCK_SIZE or self.man_x < 0 or self.man_y > self.h - BLOCK_SIZE or self.man_y < 0:
            return True
        return False

    def relative_distance(self):
        return abs(self.drone_x - self.man_x)

    def get_reward(self):
        """returns reward and done"""
        if self.is_drone_outside() or self.is_man_outside():
            return -300, True

        elif self.drone_x == self.man_x and self.drone_y == self.man_y:
            return 500, True

        else:
            return -1, False

    def step(self, action):
        self.iteration += 1
        if self.iteration % 3 == 0:
            self.man_x, self.man_y = self.man.move_man(
                self.man_x, self.man_y, 8, 'left')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.drone_x, self.drone_y = self.drone.drone_move(
            self.drone_x, self.drone_y, BLOCK_SIZE, action)

        self.reward, self.done = self.get_reward()
        return np.array([self.drone_x, self.drone_y]), self.reward, self.done

    def render(self):
        self.display.fill(GREY)

        pygame.draw.rect(self.display, self.man.color, pygame.Rect(
            self.man_x, self.man_y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, self.drone.color, pygame.Rect(
            self.drone_x, self.drone_y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()


# e = Environment()
# e.render()
