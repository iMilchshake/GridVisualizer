import numpy as np
import tkinter as tk
import random as rnd
import pygame
import math
import sys
from itertools import product


class Grid:
    """Used to read and write values to a Grid"""

    def __init__(self, width, height):
        self.height = height
        self.width = width

        # define your stored datatype here (dtype=):
        self.matrix = np.zeros((width, height), dtype=np.int32)

    def getDimensions(self):
        return self.width, self.height

    # will return whether (x,y) is inside the grid(valid)
    def valid_cell(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # will return False, if cell outside the grid is accessed
    def set(self, x, y, value):
        if self.valid_cell(x, y):
            self.matrix[x][y] = value
            return True
        else:
            return False

    # will return 'None' if a value outside the grid is accessed
    def get(self, x, y):
        if self.valid_cell(x, y):
            return self.matrix[x][y]

    # will fill the grid with random values from [a, b]
    def setRndValues(self, a, b):
        for x, y in product(range(self.width), range(self.height)):
            self.set(x, y, rnd.randint(a, b))


class Visualizer:

    # TODO: Change Grid's size while visualizing
    def __init__(self, g: Grid, window_width, window_height, border_size):
        self.g = g
        self.border_size = border_size
        self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        self.border_window_ratio = self.border_size / window_width
        self.__update_window_size(window_width, window_height)

        # default color_layout (TODO: method to change this)
        self.color_layout = {0: pygame.Color("black"),
                             1: pygame.Color("white")}

        pygame.init()

    #  updates variables, according to (new) window size
    def __update_window_size(self, window_width, window_height):
        window_width, window_height = self.get_max_grid_size(window_width, window_height)

        self.border_size = math.ceil(window_width * self.border_window_ratio)
        print(self.border_size)
        self.cell_size = min(Visualizer.get_max_cell_size(self.g.width, self.border_size, window_width),
                             Visualizer.get_max_cell_size(self.g.height, self.border_size, window_height))
        self.res_x = Visualizer.get_window_size(self.g.width, self.border_size, self.cell_size)
        self.res_y = Visualizer.get_window_size(self.g.height, self.border_size, self.cell_size)
        print((self.res_x, self.res_y), (window_width, window_height))

    #  call this to redraw the grid
    def update(self):
        self.screen.fill((255, 255, 255))
        self.__draw_grid()
        pygame.display.update()

    #  call this with pygame.event.get())
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((e.size[0], e.size[1]), pygame.RESIZABLE)
                self.__update_window_size(e.size[0], e.size[1])
                self.update()

    def __draw_grid(self):
        #  draw cells
        for x, y in product(range(self.g.width), range(self.g.height)):
            # rnd_color = (rnd.randint(1, 255), rnd.randint(1, 255), rnd.randint(1, 255))
            c = self.color_layout[self.g.get(x, y)]
            x0 = (x * (self.border_size + self.cell_size) + self.border_size)
            y0 = (y * (self.border_size + self.cell_size) + self.border_size)
            pygame.draw.rect(self.screen, c,
                             pygame.Rect(x0, y0, math.ceil(self.cell_size),
                                         math.ceil(self.cell_size)))

        # draw cell borders
        for x in range(self.g.width + 1):
            for o in range(self.border_size):
                x0 = (x * (self.border_size + self.cell_size)) + o
                pygame.draw.line(self.screen, (0, 0, 0), (x0, 0), (x0, self.res_y - 1), 1)

        for y in range(self.g.height + 1):
            for o in range(self.border_size):
                y0 = (y * (self.border_size + self.cell_size)) + o
                pygame.draw.line(self.screen, (0, 0, 0), (0, y0), (self.res_x - 1, y0), 1)

    @staticmethod
    def get_max_cell_size(cell_count, border_size, window_size):
        return math.floor(window_size - ((cell_count + 1) * border_size)) / cell_count

    @staticmethod
    def get_window_size(cell_count, border_size, cell_size):
        return ((cell_count + 1) * border_size) + (cell_count * cell_size)

    def get_max_grid_size(self, w, h):
        h_size = Visualizer.get_max_cell_size(self.g.width, self.border_size, w)
        v_size = Visualizer.get_max_cell_size(self.g.height, self.border_size, h)
        if h_size < v_size:
            new_h = Visualizer.get_window_size(self.g.height, self.border_size, h_size)
            return w, new_h
        else:
            new_w = Visualizer.get_window_size(self.g.width, self.border_size, v_size)
            return new_w, h
