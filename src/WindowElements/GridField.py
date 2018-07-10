import pyglet
from pyglet.gl import gl


class GridField:
    def __init__(self, size_cell, start_point, size_grid, color):
        self.size_cell = size_cell
        self.start_point = start_point
        self.size_grid = size_grid
        self.color = color

        self.batch = pyglet.graphics.Batch()
        self.lines = pyglet.graphics.Batch()

        line_color = tuple(self.color) * 4
        self.lines.add(4, gl.GL_LINES, None,
                       ('v2i', (0, -500, 0, 500,  # start -> end
                                -500, 0, 500, 0)),  # start -> end

                       ('c4B', line_color)
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
        pyglet.gl.glLineWidth(3)
        self.lines.draw()
        pyglet.gl.glLineWidth(1)
