from src.GameElements.Items.Item import ItemClass
from src.Constants import *
import random


class ItemController:
    screen = None
    map = None
    game_controller = None

    def __init__(self, game_controller):
        self.game_controller = game_controller

    def create_meat(self, position, batch):
        item = ItemClass(self.game_controller, batch, 'meat', position, (1, 1), meat_image)
        item.set_edible(True)
        item.set_stat('satiety', 15)

        return item

    def generate_items_around(self, point, radius=2, speed=2):
        if self.game_controller.get_time() % speed == 0:
            rand_x = random.randint((-1) * radius, radius)
            rand_y = random.randint((-1) * radius, radius)
            cell = self.get_cell(rand_x, rand_y)

            while not cell.is_passable():
                rand_x = random.randint((-1) * radius, radius)
                rand_y = random.randint((-1) * radius, radius)
                cell = self.get_cell(rand_x, rand_y)

            self.create_meat((point[0] + rand_x, point[1] + rand_y))

    def is_item(self, game_object):
        return isinstance(game_object, ItemClass)
