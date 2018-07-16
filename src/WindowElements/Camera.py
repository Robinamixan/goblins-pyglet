import pyglet
from pyglet.gl import *

# Zooming constants
ZOOM_IN_FACTOR = 1.2
ZOOM_OUT_FACTOR = 1/ZOOM_IN_FACTOR


class Camera:
    def __init__(self, width, height):
        # Initialize camera values
        self.left = 0
        self.right = width
        self.bottom = 0
        self.top = height
        self.zoom_level = 1
        self.zoomed_width = width
        self.zoomed_height = height

        self.vect_x = 0
        self.vect_y = 0

    def draw(self):
        glOrtho(self.left, self.right, self.bottom, self.top, 1, -1)

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pre_left = self.left - dx * self.zoom_level
        pre_right = self.right - dx * self.zoom_level
        pre_bottom = self.bottom - dy * self.zoom_level
        pre_top = self.top - dy * self.zoom_level

        valid = True
        if -1000 >= pre_left or pre_left >= 1500:
            valid = False
        if -1000 >= pre_right or pre_right >= 1500:
            valid = False
        if -1000 >= pre_bottom or pre_bottom >= 1000:
            valid = False
        if -1000 >= pre_top or pre_top >= 1000:
            valid = False

        if valid:
            self.left = pre_left
            self.right = pre_right
            self.bottom = pre_bottom
            self.top = pre_top

    def update(self):
        pre_left = self.left - self.vect_x * self.zoom_level
        pre_right = self.right - self.vect_x * self.zoom_level
        pre_bottom = self.bottom - self.vect_y * self.zoom_level
        pre_top = self.top - self.vect_y * self.zoom_level

        valid = True
        if -1000 >= pre_left or pre_left >= 2000:
            valid = False
        if -1000 >= pre_right or pre_right >= 2000:
            valid = False
        if -1000 >= pre_bottom or pre_bottom >= 1000:
            valid = False
        if -1000 >= pre_top or pre_top >= 1500:
            valid = False

        if valid:
            self.left = pre_left
            self.right = pre_right
            self.bottom = pre_bottom
            self.top = pre_top

    def set_move_vertical(self, move_y):
        self.vect_y = move_y

    def set_move_horizontal(self, move_x):
        self.vect_x = move_x

    def mouse_scroll(self, x, y, dx, dy, width, height):
        # Get scale factor
        f = ZOOM_OUT_FACTOR if dy > 0 else ZOOM_IN_FACTOR if dy < 0 else 1
        # If zoom_level is in the proper range
        if .2 < self.zoom_level * f < 5:
            self.zoom_level *= f

            mouse_x = x / width
            mouse_y = y / height

            mouse_x_in_world = self.left + mouse_x * self.zoomed_width
            mouse_y_in_world = self.bottom + mouse_y * self.zoomed_height

            self.zoomed_width *= f
            self.zoomed_height *= f

            self.left = mouse_x_in_world - mouse_x * self.zoomed_width
            self.right = mouse_x_in_world + (1 - mouse_x) * self.zoomed_width
            self.bottom = mouse_y_in_world - mouse_y * self.zoomed_height
            self.top = mouse_y_in_world + (1 - mouse_y) * self.zoomed_height

    def get_zoom_level(self):
        return round(self.zoom_level, 2)
