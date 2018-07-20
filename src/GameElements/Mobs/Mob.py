from src.GameElements.GameObject import GameObject
from src.GameElements.Inventory.Inventory import InventoryClass
from pyglet.gl import gl
import copy
import random
from src.Constants import *


class MobClass(GameObject):
    def __init__(self, game_controller, batch, name, point, size, speed, inventory_size, image_path):
        super().__init__(game_controller, batch, name, point, size, image_path)
        self.vectors = [0, 0]

        self.destination = self.point
        self.path = []
        self.wait_index = 0
        self.wait_path_index = 0
        self.target = []
        self.passable = False

        self.speed = speed
        self.actions = {
            'wait': 'waiting',
            'wait_clear': 'waiting clear path',
            'move': 'going',
            'get': 'getting',
            'return': 'return to base'
        }
        self.action = 'wait'
        self.inventory = InventoryClass(inventory_size)

    # Get destination cell by current destination coord
    def get_destination_cell(self):
        return self.game_controller.get_cell(self.destination)

    def get_destination(self):
        return self.destination

    def get_vectors(self):
        return self.vectors

    def get_inventory_info(self):
        return self.inventory.get_info()

    # Getting current acts of mob
    def get_action(self):
        return self.action

    def get_action_string(self):
        return self.actions[self.action]

    def get_target(self):
        return self.target

    def get_wait_index(self):
        return self.wait_index

    def get_wait_path_index(self):
        return self.wait_path_index

    def set_point_as_destination(self, index=None):
        if index is not None:
            self.point[index] = copy.copy(self.destination[index])
        else:
            self.point = copy.copy(self.destination)

    def set_destination(self, point):
        self.destination = list(point)

    def set_target(self, point, recreating=False):
        self.target = point
        self.create_path(self.destination, self.target, recreating)
        if self.target:
            cell = self.game_controller.get_cell(self.target)
            if cell.is_empty():
                self.set_action('move')
            else:
                self.set_action('get')
                if self.destination == self.target:
                    self.catch_item()

    def set_action(self, action):
        if action in self.actions.keys():
            self.action = action

    def set_vector(self, index, first_number, second_number):
        if first_number > second_number:
            self.vectors[index] = -1
        elif first_number < second_number:
            self.vectors[index] = 1
        else:
            self.vectors[index] = 0

    def update_action(self):
        if self.get_action() == 'wait_clear':
            if self.get_point() != self.get_destination():
                if self.target:
                    cell = self.game_controller.get_cell(self.target)
                    if cell.is_empty():
                        self.set_action('move')
                    else:
                        self.set_action('get')
                        if self.destination == self.target:
                            self.catch_item()

    def update_conditions(self):
        if self.get_action() == 'wait':
            self.wait_index += 1
        elif self.get_action() == 'wait_clear':
            self.wait_path_index += 1
        else:
            self.wait_index = 0
            self.wait_path_index = 0

    def update(self, dt):
        if self.path:
            if self.destination == self.point:
                self.go_to_next_step(dt)
            else:
                self.update_move(dt)
        else:
            self.stop()

    def go_to_next_step(self, dt):
        if self.path[0] == self.destination:
            self.path.pop(0)

        next_step = self.path[0]
        next_cell = self.game_controller.get_cell(next_step)

        if next_cell.is_can_move(self):
            self.game_controller.remove_object_from_cell(self.point, self)
            next_cell.set_object(self)
            self.destination = next_step
            self.update_move(dt)
            self.update_sprite_image()
            self.update_action()
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
        self.update_sprite_image()

        if self.path:
            self.set_action('wait_clear')
            if self.get_wait_path_index() > random.randint(1, 3):
                self.set_target(self.target, recreating=True)
        elif self.get_action() == 'get':
            self.catch_item()
        else:
            self.target = []
            self.set_action('wait')

    # Creating move path by start and end points
    def create_path(self, start, end, recreating=False):
        path = self.game_controller.create_path(start, end, recreating)
        if path:
            self.path = path
        elif self.path:
            self.path = [self.path[0]]

    # calculate next point by frame
    def get_next_position(self, dt):
        next_x = self.sprite.x + dt * self.vectors[0] * 10 * self.speed
        next_y = self.sprite.y + dt * self.vectors[1] * 10 * self.speed

        return next_x, next_y

    def update_sprite_image(self):
        if self.vectors[0] == 0:
            if self.vectors[1] == 1:
                self.sprite.image = goblin_image_back
            else:
                self.sprite.image = goblin_image_front

        if self.vectors[0] == 1:
            self.sprite.image = goblin_image_right

        if self.vectors[0] == -1:
            self.sprite.image = goblin_image_left
        self.sprite.update()

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

    def catch_item(self):
        cell = self.get_destination_cell()
        items = copy.copy(cell.contain)
        items.remove(self)
        for item in items:
            if self.get_item(item):
                self.game_controller.remove_item(item)
        self.set_action('wait')

    def get_item(self, item):
        if self.game_controller.is_item(item):
            return self.inventory.add_items(item, 1)
        else:
            return False

    def remove_item(self, item):
        return self.inventory.delete_items(item, 1)

    def remove_items(self, item, amount):
        return self.inventory.delete_items(item, amount)

    def is_inventory_full(self):
        return self.inventory.is_full()

    def is_waiting(self):
        return self.get_action() == 'wait'

    def is_waiting_path(self):
        return self.get_action() == 'wait_clear'

