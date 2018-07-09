from src.GameElements.GameObject import GameObject
from pyglet.gl import gl
import copy
from src.Constants import *


class MobClass(GameObject):
    def __init__(self, game_controller, batch, name, point, size, speed, image_path):
        super().__init__(game_controller, batch, name, point, size, image_path)
        self.vectors = [0, 0]

        self.destination = self.point
        self.path = []

        self.speed = speed

    # Get destination cell by current destination coord
    def get_destination_cell(self):
        return self.game_controller.get_cell(self.destination)

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

    def set_point_as_destination(self, index=None):
        if index is not None:
            self.point[index] = copy.copy(self.destination[index])
        else:
            self.point = copy.copy(self.destination)

    def set_target(self, point):
        self.create_path(self.destination, point)

    def set_vector(self, index, first_number, second_number):
        if first_number > second_number:
            self.vectors[index] = -1
        elif first_number < second_number:
            self.vectors[index] = 1
        else:
            self.vectors[index] = 0

    def update(self, dt):
        if self.path:
            if self.destination == self.point:
                self.go_to_next_step(dt)
            else:
                self.update_move(dt)
        else:
            self.stop()

    def go_to_next_step(self, dt):
        if self.path[0] == self.point:
            self.path.pop(0)

        next_step = self.path[0]
        next_cell = self.game_controller.get_cell(next_step)

        if next_cell.is_can_move(self):
            self.game_controller.remove_object_from_cell(self.point, self)
            next_cell.set_object(self)
            self.destination = next_step
            self.update_move(dt)
        else:
            self.stop()

    def update_move(self, dt):
        cell = self.get_destination_cell()
        if self.is_destination_x(cell) and self.is_destination_y(cell):
            self.set_point_as_destination()
            self.path.pop(0)
            self.update_vectors_in_wait_position()
        else:
            if self.is_destination_x(cell):
                self.set_coord_x(cell.x)
                self.set_point_as_destination(0)

            if self.is_destination_y(cell):
                self.set_coord_y(cell.y)
                self.set_point_as_destination(1)

            self.update_vectors(cell)
            self.set_coord(self.get_next_position(dt))

    def is_destination_x(self, cell):
        if self.destination[0] > self.point[0]:
            return self.x >= cell.x
        else:
            return self.x <= cell.x

    def is_destination_y(self, cell):
        if self.destination[1] > self.point[1]:
            return self.y >= cell.y
        else:
            return self.y <= cell.y

    def update_vectors(self, cell):
        self.set_vector(0, self.x, cell.x)
        self.set_vector(1, self.y, cell.y)

        if self.vectors[0] == 0 and self.vectors[1] == 0:
            self.update_vectors_in_wait_position()

    def update_vectors_in_wait_position(self):
        if self.path:
            next_destin = self.path[0]

            self.set_vector(0, self.point[0], next_destin[0])
            self.set_vector(1, self.point[1], next_destin[1])

    # stop moving and set coord
    def stop(self):
        self.set_coord(self.game_controller.get_coord_by_point(self.destination))
        self.set_point_as_destination()
        self.vectors = [0, 0]

    # Creating move path by start and end points
    def create_path(self, start, end):
        path = []
        step_number = 0
        current_step = copy.copy(list(start))

        while end != current_step:
            path.append([current_step[0], current_step[1]])

            if self.path and step_number == 0:
                step_number += 1
                continue

            for index, i in enumerate(current_step):
                if current_step[index] < end[index]:
                    current_step[index] += 1
                elif current_step[index] > end[index]:
                    current_step[index] -= 1
                path[step_number][index] = current_step[index]
            step_number += 1

        self.path = path

    # calculate next point by frame
    def get_next_position(self, dt):
        next_x = self.sprite.x + dt * self.vectors[0] * 10 * self.speed
        next_y = self.sprite.y + dt * self.vectors[1] * 10 * self.speed

        return next_x, next_y

    def draw_path(self):
        if self.path:
            for point in self.path:
                cell = self.game_controller.get_cell(point)

                start_x = cell.x
                start_y = cell.y

                end_x = start_x + cell.size
                end_y = start_y + cell.size

                pyglet.graphics.draw(
                    4,
                    gl.GL_POLYGON,
                    ('v2i', [start_x, start_y, start_x, end_y, end_x, end_y, end_x, start_y]),
                    ('c4B', red_alpha * 4))
