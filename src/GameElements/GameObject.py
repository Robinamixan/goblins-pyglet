import pyglet
from src.Constants import *


class GameObject:
    def __init__(self, game_controller, batch, name, point, size, image):
        self.game_controller = game_controller

        self.name = name
        self.point = list(point)
        self.passable = False

        position = self.game_controller.get_coord_by_point(point)
        self.x = position[0]
        self.y = position[1]

        self.width = size[0] * map_cell_size
        self.height = size[1] * map_cell_size
        self.sprite = pyglet.sprite.Sprite(image, x=self.x, y=self.y, batch=batch)
        self.sprite.image.width = self.width
        self.sprite.image.height = self.height

    def get_coord(self):
        return self.sprite.position

    def get_point(self):
        return self.point

    def get_size(self):
        return [self.width, self.height]

    def get_relative_size(self):
        return [int(self.width / map_cell_size), int(self.height / map_cell_size)]

    def get_name(self):
        return self.name

    def is_inside(self, point):
        horizontal = self.x <= point[0] <= self.x + self.width
        vertical = self.y <= point[1] <= self.y + self.height

        return horizontal and vertical

    def draw(self):
        self.sprite.draw()

    def delete(self):
        self.sprite.delete()
