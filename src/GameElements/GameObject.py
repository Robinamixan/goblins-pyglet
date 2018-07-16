import pyglet
from src.Constants import *


class GameObject:
    def __init__(self, game_controller, batch, name, point, size, image):
        self.game_controller = game_controller

        self.name = name
        self.point = list(point)
        self.passable = False

        coord = self.game_controller.get_coord_by_point(point)
        self.x = coord[0]
        self.y = coord[1]

        self.width = size[0] * map_cell_size
        self.height = size[1] * map_cell_size
        self.sprite = pyglet.sprite.Sprite(image, x=self.x, y=self.y, batch=batch)
        self.sprite.image.width = self.width
        self.sprite.image.height = self.height
        self.sprite.update()

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

    def get_stat(self, stat):
        if hasattr(self, stat):
            return getattr(self, stat)

    def get_visible(self):
        return self.sprite.visible

    def is_inside(self, point):
        horizontal = self.x <= point[0] <= self.x + self.width
        vertical = self.y <= point[1] <= self.y + self.height

        return horizontal and vertical

    def get_around_points(self):
        start_point = [self.point[0] - 1, self.point[1] - 1]

        size = self.get_relative_size()
        end_point = [self.point[0] + size[0], self.point[1] + size[1]]

        object_points = []
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                object_points.append([self.point[0] + i, self.point[1] + j])

        around_points = []
        for i in range(start_point[0], end_point[0] + 1):
            for j in range(start_point[1], end_point[1] + 1):
                if [i, j] not in object_points:
                    around_points.append([i, j])

        return around_points

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        pass

    def delete(self):
        self.sprite.delete()

    def set_stat(self, stat, value):
        if hasattr(self, stat):
            setattr(self, stat, value)

    def set_point(self, point):
        self.point = point
        self.set_coord(self.game_controller.get_coord_by_point(point))

    def set_coord(self, coord):
        self.sprite.x = coord[0]
        self.sprite.y = coord[1]
        self.x = self.sprite.x
        self.y = self.sprite.y

    def set_coord_x(self, x):
        self.sprite.x = x
        self.x = self.sprite.x

    def set_coord_y(self, y):
        self.sprite.y = y
        self.y = self.sprite.y

    def set_visible(self, visible):
        self.sprite.visible = visible
