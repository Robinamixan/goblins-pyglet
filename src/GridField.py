import pyglet
from pyglet.gl import gl


class GridField:
    def __init__(self, size_cell, start_point, size_grid, color):
        self.size_cell = size_cell
        self.start_point = start_point
        self.size_grid = size_grid
        self.color = color

        self.batch = pyglet.graphics.Batch()

        self.batch.add(4, gl.GL_LINES, None,
                       ('v2i', (0, -500, 0, 500,  # start -> end
                                -500, 0, 500, 0)),  # start -> end

                       ('c3B', (0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0))
                       )

        color = tuple(self.color) * 8
        for x in range(self.size_grid[0]):
            for y in range(self.size_grid[1]):
                start_x = self.start_point[0] + self.size_cell * x
                start_y = self.start_point[1] + self.size_cell * y

                end_x = start_x + self.size_cell
                end_y = start_y + self.size_cell

                self.batch.add(
                    8,
                    gl.GL_LINES,
                    None,
                    ('v2i', (
                        start_x, start_y, end_x, start_y,  # start -> end
                        end_x, start_y, end_x, end_y,
                        end_x, end_y, start_x, end_y,
                        start_x, end_y, start_x, start_y,
                    )),
                    ('c4B', color)
                               )

    def draw(self):
        self.batch.draw()
