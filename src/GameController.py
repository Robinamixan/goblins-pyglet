from src.GameElements.Mobs.MobsController import MobsController
from src.GameElements.Items.ItemsController import ItemController
from src.GameElements.Map.MapClass import MapClass
from src.GameElements.Map.PathCreator import PathCreator
from src.Constants import *
import copy
import pyglet


class GameController:
    def __init__(self):
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

    def set_focus(self, mouse_position):
        point = self.get_point_by_coord(mouse_position)
        map_object = self.map.get_cell_object(point)

        self.focused = map_object

    def draw_focus(self):
        if self.mob_controller.is_mob(self.focused):
            self.focused.draw_path()

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

    def create_gob(self, name, point):
        gob = self.mob_controller.create_gob(name, point, self.mobs_bath)
        self.add_mob(gob)
        self.add_object_in_cell(point, gob)

    def set_focus_target(self, coord):
        if self.mob_controller.is_mob(self.focused):
            point = self.get_point_by_coord(coord)
            self.focused.set_target(point)

    def create_path(self, start, end):
        return self.path_creator.create_path(start, end)
    # MOBS FUNCTIONS

    # STATIC OBJECTS FUNCTIONS
    def create_wall(self, point):
        wall = self.map.create_wall(point)
        self.add_static_object(wall)
        self.add_object_in_cell(point, wall)

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

    def draw_items(self):
        self.items_bath.draw()

    def remove_item(self, item_object):
        self.items_group.remove(item_object)
        item_object.delete()
        self.remove_object_from_cell(item_object.get_point(), item_object)

        if self.focused == item_object:
            self.focused = None
    # ITEM FUNCTIONS
