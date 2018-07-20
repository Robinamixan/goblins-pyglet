from src.GameElements.Map.Cell import CellClass
from src.GameElements.Static.Wall import WallClass
from src.GameElements.Static.Tree import TreeClass
from src.GameElements.Static.MainBuilding import MainBuildingClass
from src.Constants import *
from pyglet.gl import gl
import pyglet


class MapClass:
    def __init__(self, title, game_controller, position, cell_size, map_size):
        self.title = title
        self.game_controller = game_controller
        self.cells_batch = pyglet.graphics.Batch()
        self.walls_batch = pyglet.graphics.Batch()
        self.trees_batch = pyglet.graphics.Batch()
        self.buildings_batch = pyglet.graphics.Batch()
        self.lines_batch = pyglet.graphics.Batch()

        self.x = position[0]
        self.y = position[1]
        self.cell_size = cell_size
        self.map_size = map_size
        self.cells = []

        self.set_cells_grid()
        self.set_map_borders()

    def draw(self):
        self.cells_batch.draw()
        pyglet.gl.glLineWidth(3)
        self.lines_batch.draw()
        pyglet.gl.glLineWidth(1)
        self.walls_batch.draw()
        self.trees_batch.draw()
        self.buildings_batch.draw()

    def create_wall(self, point):
        return WallClass(self.game_controller, self.walls_batch, 'wall_' + str(point[0]) + '_' + str(point[1]), point, (1, 1), wall_image)

    def create_tree(self, point):
        return TreeClass(self.game_controller, self.trees_batch, 'tree_' + str(point[0]) + '_' + str(point[1]), point, (2, 2), tree_image)

    def create_cave(self, point):
        return MainBuildingClass(self.game_controller, self.buildings_batch, 'cave_' + str(point[0]) + '_' + str(point[1]), point, (2, 2), cave_image)

    def is_wall(self, game_object):
        return isinstance(game_object, WallClass)

    def is_tree(self, game_object):
        return isinstance(game_object, TreeClass)

    def is_cave(self, game_object):
        return isinstance(game_object, MainBuildingClass)

    def create_map_from_file(self, file_name):
        file = open(file_name, 'r')
        strings_map = [''] * self.map_size[1]
        ind_y = self.map_size[1] - 1
        ind_x = 0
        for line in file:
            strings_map[ind_y] = line
            ind_y -= 1
        file.close()

        for index_y, line in enumerate(strings_map):
            for index_x, character in enumerate(line):
                if character == '\n':
                    continue
                if character == 'w':
                    self.game_controller.create_wall((index_x, index_y))
                if character == 't':
                    if self.map_has_full_object([index_x, index_y], [2, 2], character, strings_map):
                        self.game_controller.create_tree((index_x, index_y))
                if character == 'c':
                    if self.map_has_full_object([index_x, index_y], [2, 2], character, strings_map):
                        self.game_controller.create_cave((index_x, index_y))

    def map_has_full_object(self, start_point, size, character, string_map):
        for x in range(start_point[0], start_point[0] + size[0]):
            for y in range(start_point[1], start_point[1] + size[1]):
                if string_map[y][x] != character:
                    return False

        return True

    def get_cell(self, x, y):
        return self.cells[x][y]

    def get_cell_object(self, point):
        cell = self.get_cell(point[0], point[1])
        return cell.get_object()

    def add_object_in_cell(self, point, map_object, passable=False):
        cell = self.get_cell(point[0], point[1])
        cell.set_object(map_object, passable)

    def remove_object_from_cell(self, point, map_object):
        cell = self.get_cell(point[0], point[1])
        cell.remove_object(map_object)

    def get_coord_by_point(self, x, y):
        coord = [int(x * self.cell_size + self.x), int(y * self.cell_size + self.y)]
        return coord

    def get_point_by_coord(self, x, y):
        point = [int((x - self.x) / self.cell_size), int((y - self.y) / self.cell_size)]

        if point[0] >= self.map_size[0]:
            point[0] = self.map_size[0] - 1

        if point[1] >= self.map_size[1]:
            point[1] = self.map_size[1] - 1

        if point[0] < 0:
            point[0] = 0

        if point[1] < 0:
            point[1] = 0

        return point

    def set_cells_grid(self):
        self.cells = [0] * self.map_size[0]
        color = tuple(black) * 8
        for i in range(0, self.map_size[0]):
            self.cells[i] = [None] * self.map_size[1]
            for j in range(0, self.map_size[1]):
                point = self.get_coord_by_point(i, j)
                self.cells[i][j] = CellClass(point[0], point[1], self.cell_size, grass_image, self.cells_batch)

                start_x = self.x + self.cell_size * i
                start_y = self.y + self.cell_size * j

                end_x = start_x + self.cell_size
                end_y = start_y + self.cell_size

                # self.cells_batch.add(
                #     8,
                #     gl.GL_LINES,
                #     None,
                #     ('v2i', (
                #         start_x, start_y, end_x, start_y,  # start -> end
                #         end_x, start_y, end_x, end_y,
                #         end_x, end_y, start_x, end_y,
                #         start_x, end_y, start_x, start_y,
                #     )),
                #     ('c4B', color)
                # )

    def set_map_borders(self):
        line_color = tuple(red) * 8
        end_x = self.x + self.cell_size * self.map_size[0]
        end_y = self.y + self.cell_size * self.map_size[1]
        self.lines_batch.add(8, gl.GL_LINES, None,
                             ('v2i', (
                                 self.x, self.y, self.x, end_y,  # start -> end
                                 self.x, end_y, end_x, end_y,  # start -> end
                                 end_x, end_y, end_x, self.y,  # start -> end
                                 end_x, self.y, self.x, self.y,  # start -> end
                             )),

                             ('c4B', line_color)
                             )
