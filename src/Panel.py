import pyglet
from pyglet.gl import gl


class Panel:
    def __init__(self, window, start_point, end_point, color):
        self.window = window
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.batch = pyglet.graphics.Batch()

        start_x = self.start_point[0]
        start_y = self.start_point[1]

        end_x = self.end_point[0]
        end_y = self.end_point[1]

        self.batch.add(
            4,
            gl.GL_POLYGON,
            None,
            ('v2i', [start_x, start_y, start_x, end_y, end_x, end_y, end_x, start_y]),
            ('c4B', self.color * 4))

    def draw(self):
        """Draw the label.

        The OpenGL state is assumed to be at default values, except
        that the MODELVIEW and PROJECTION matrices are ignored.  At
        the return of this method the matrix mode will be MODELVIEW.
        """
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, self.window.width, 0, self.window.height, -1, 1)

        self.batch.draw()

        gl.glPopMatrix()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
