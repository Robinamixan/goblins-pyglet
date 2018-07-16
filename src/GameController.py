from src.GameElements.Mobs.MobsController import MobsController
from src.GameElements.Items.ItemsController import ItemController
from src.GameElements.Map.Map import MapClass
from src.GameElements.Map.PathCreator import PathCreator
from src.Constants import *
import copy
import pyglet
import random
import math


class GameController:
    def __init__(self):
        self.timer = 0
        self.mobs_group = []
        self.static_group = []
        self.items_group = []
        self.mobs_bath = pyglet.graphics.Batch()
        self.items_bath = pyglet.graphics.Batch()
        self.focused = None
        self.mob_controller = MobsController(self)
        self.item_controller = ItemController(self)
        self.map = MapClass('map', self, (100, 30), map_cell_size, (30, 30))
        self.map.create_map_from_file('GameElements/Map/templates/test_map_2.txt')
        self.path_creator = PathCreator(self.map)

    def set_timer(self, time):
        self.timer = time

    def get_timer(self):
        return self.timer

    def get_distance_between(self, point_1, point_2):
        return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

    def set_focus(self, mouse_position):
        point = self.get_point_by_coord(mouse_position)
        map_object = self.map.get_cell_object(point)

        self.focused = map_object

    def draw_focus(self):
        if self.is_mob(self.focused):
            self.focused.draw_path()

    def set_focus_target(self, coord):
        if self.is_mob(self.focused):
            point = self.get_point_by_coord(coord)
            self.focused.set_target(point)

        if self.is_cave(self.focused):
            cave = self.focused
            cave.send_member()

    def get_focused(self):
        return self.focused

    def get_cell(self, point):
        return self.map.get_cell(point[0], point[1])

    def get_coord_by_point(self, point):
        return self.map.get_coord_by_point(point[0], point[1])

    def get_point_by_coord(self, coord):
        return self.map.get_point_by_coord(coord[0], coord[1])

    def add_object_in_cell(self, point, game_object, passable=False):
        size = game_object.get_relative_size()
        if size == [1, 1]:
            self.map.add_object_in_cell(point, game_object, passable)
        else:
            start_point = copy.copy(point)
            points = []
            for i in range(size[0]):
                for j in range(size[1]):
                    points.append([i + start_point[0], j + start_point[1]])

            for point in points:
                self.map.add_object_in_cell(point, game_object, passable)

    def remove_object_from_cell(self, point, game_object):
        self.map.remove_object_from_cell(point, game_object)

    # MOBS FUNCTIONS
    def is_mob(self, game_object):
        return self.mob_controller.is_mob(game_object)

    def add_mob(self, mob_object):
        self.mobs_group.append(mob_object)

    def remove_mob(self, mob_object):
        self.mobs_group.remove(mob_object)
        mob_object.delete()
        self.remove_object_from_cell(mob_object.get_point(), mob_object)

        if self.focused == mob_object:
            self.focused = None

    def update_mobs(self, dt):
        for mob in self.mobs_group:
            mob.update(dt)

    def draw_mobs(self):
        self.mobs_bath.draw()

    def create_gob(self, name, point, add_to_cell=True):
        gob = self.mob_controller.create_gob(name, point, self.mobs_bath)
        self.add_mob(gob)
        if add_to_cell:
            self.add_object_in_cell(point, gob)

        return gob

    def create_path(self, start, end):
        return self.path_creator.create_path(start, end)
    # MOBS FUNCTIONS

    # STATIC OBJECTS FUNCTIONS
    def create_wall(self, point):
        wall = self.map.create_wall(point)
        self.add_static_object(wall)
        self.add_object_in_cell(point, wall)

    def create_tree(self, point):
        tree = self.map.create_tree(point)
        self.add_static_object(tree)
        self.add_object_in_cell(point, tree)

    def create_cave(self, point):
        cave = self.map.create_cave(point)

        self.add_static_object(cave)
        self.add_object_in_cell(point, cave)

    def add_static_object(self, static_object):
        self.static_group.append(static_object)

    def remove_static_object(self, static_object):
        self.static_group.remove(static_object)
        static_object.delete()
        self.remove_object_from_cell(static_object.get_point(), static_object)

        if self.focused == static_object:
            self.focused = None

    def draw_map(self):
        self.map.draw()

    def is_cave(self, game_object):
        return self.map.is_cave(game_object)

    def update_static(self, dt):
        for static in self.static_group:
            static.update(dt)
    # STATIC OBJECTS FUNCTIONS

    # ITEM FUNCTIONS
    def is_item(self, game_object):
        return self.item_controller.is_item(game_object)

    def add_item(self, item_object):
        self.items_group.append(item_object)

    def create_meat(self, point):
        meat = self.item_controller.create_meat(point, self.items_bath)
        self.add_item(meat)
        self.add_object_in_cell(point, meat, passable=True)

    def create_apple(self, point):
        apple = self.item_controller.create_apple(point, self.items_bath)
        self.add_item(apple)
        self.add_object_in_cell(point, apple, passable=True)

    def draw_items(self):
        self.items_bath.draw()

    def remove_item(self, item_object):
        self.items_group.remove(item_object)
        item_object.delete()
        self.remove_object_from_cell(item_object.get_point(), item_object)

        if self.focused == item_object:
            self.focused = None

    def generate_items_around(self, point, radius=2, speed=2):
        self.item_controller.generate_items_around(point, radius, speed)

    def get_food_item(self, point=None, excepts=None):
        available_items = [e for e in self.items_group if e.get_point() not in excepts]
        if available_items:
            if point:
                min_distance = self.get_distance_between(point, available_items[0].get_point())
                nearest_index = False
                for index, item in enumerate(available_items):
                    distance = self.get_distance_between(point, item.get_point())
                    if distance <= min_distance:
                        min_distance = distance
                        nearest_index = index
                if nearest_index is not False:
                    return available_items[nearest_index]
                else:
                    return None
            else:
                return random.choice(available_items)
    # ITEM FUNCTIONS
