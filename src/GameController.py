from src.GameElements.Mobs.MobsController import MobsController
from src.GameElements.Map.Map import Map
from src.GameElements.Map.PathCreator import PathCreator
from src.Constants import *
import copy
import pyglet


class GameController:
    def __init__(self):
        self.mobs_group = []
        self.mobs_bath = pyglet.graphics.Batch()
        self.static_objects = []
        self.focused = None
        self.mob_controller = MobsController(self)
        self.map = Map('map', self, (100, 30), map_cell_size, (30, 30))
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

    def add_object_in_cell(self, point, game_object):
        size = game_object.get_relative_size()
        if size == [1, 1]:
            self.map.add_object_in_cell(point, game_object)
        else:
            start_point = copy.copy(point)
            points = []
            for i in range(size[0]):
                for j in range(size[1]):
                    points.append([i + start_point[0], j + start_point[1]])

            for point in points:
                self.map.add_object_in_cell(point, game_object)

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
        point = self.get_point_by_coord(coord)
        if self.mob_controller.is_mob(self.focused):
            self.focused.set_target(point)

    def create_path(self, start, end):
        return self.path_creator.create_path(start, end)
    # MOBS FUNCTIONS

    # STATIC OBJECTS FUNCTIONS
    def create_wall(self, point):
        wall = self.map.create_wall(point)
        self.add_static_object(wall)
        self.add_object_in_cell(point, wall)

    def add_static_object(self, static):
        self.static_objects.append(static)

    def remove_static_object(self, static):
        self.static_objects.remove(static)
        static.delete()

        if self.focused == static:
            self.focused = None

    def draw_map(self):
        self.map.draw()
    # STATIC OBJECTS FUNCTIONS
