import pyglet
from pyglet.gl import gl


class FixedLabel:
    def __init__(self, window, text, position, color=(255, 255, 255, 255), font_size=24, fixed_bottom=True, fixed_left=True):
        from pyglet.text import Label
        self.position = position
        self.window = window
        self.fixed_bottom = fixed_bottom
        self.fixed_left = fixed_left
        self.color = color

        if self.fixed_bottom:
            pos_y = self.position[1]
        else:
            pos_y = self.window.height - self.position[1]

        if self.fixed_left:
            pos_x = self.position[0]
        else:
            pos_x = self.window.width - self.position[0]

        self.label = Label(text, x=pos_x, y=pos_y,
                           font_size=font_size, bold=True,
                           color=self.color)

    def update(self, text):
        self.label.text = text
        if self.fixed_bottom:
            self.label.y = self.position[1]
        else:
            self.label.y = self.window.height - self.position[1]

        if self.fixed_left:
            self.label.x = self.position[0]
        else:
            self.label.x = self.window.width - self.position[0]

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

        self.label.draw()

        gl.glPopMatrix()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
