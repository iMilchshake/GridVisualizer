import numpy as np
import tkinter as tk
import random as rnd
import pygame
import math
import sys


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


class Visualizer:

    # TODO: Change Grid's size while visualizing
    # TODO: Dynamic border_size
    def __init__(self, g: Grid, window_width, window_height, border_size):
        self.g = g  # Grid to
        self.border_size = border_size
        self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        self.__update_window_size(window_width, window_height)
        pygame.init()

    #  updates variables, according to (new) window size
    def __update_window_size(self, window_width, window_height):
        self.cell_size = min(Visualizer.get_max_cell_size(self.g.width, self.border_size, window_width),
                             Visualizer.get_max_cell_size(self.g.height, self.border_size, window_height))
        self.res_x = Visualizer.get_window_size(self.g.width, self.border_size, self.cell_size)
        self.res_y = Visualizer.get_window_size(self.g.height, self.border_size, self.cell_size)

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
        return (window_size - ((cell_count + 1) * border_size)) / cell_count

    @staticmethod
    def get_window_size(cell_count, border_size, cell_size):
        return ((cell_count + 1) * border_size) + (cell_count * cell_size)
