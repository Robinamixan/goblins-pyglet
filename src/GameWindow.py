import pyglet
from pyglet.gl import *
from pyglet.window import key, FPSDisplay
from src.MobClass import MobClass
from src.Camera import Camera
from src.GridField import GridField
from src.FixedLabel import FixedLabel
from src.Panel import Panel
from src.Constants import *


class GameWindow(pyglet.window.Window):
    def __init__(self, width, height, *args, **kwargs):
        conf = Config(sample_buffers=1,
                      samples=4,
                      depth_size=16,
                      double_buffer=True)

        super().__init__(config=conf, width=width, height=height, *args, **kwargs)
        self.window_settings()

        self.camera = Camera(width, height)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.fps_display = FPSDisplay(self)
        self.show_info = False
        self.frame_rate = 1 / 60.0
        pyglet.clock.schedule_interval(self.update, self.frame_rate)

        self.gob = MobClass(x=150, y=150)
        self.grid = GridField(25, (100, 100), (10, 10), black)
        self.panel = Panel(self, (self.width - 250, 0), (self.width, self.height), gray)

        self.zoom_level = FixedLabel(self, str(self.camera.get_zoom_level()), (10, 35), color=black, fixed_bottom=False)

    def update(self, dt):
        self.gob.update(dt)
        self.camera.update()
        self.zoom_level.update(str(self.camera.get_zoom_level()))

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.W:
            self.camera.set_move_vertical(-5)
        elif KEY == key.S:
            self.camera.set_move_vertical(5)
        elif KEY == key.A:
            self.camera.set_move_horizontal(5)
        elif KEY == key.D:
            self.camera.set_move_horizontal(-5)
        elif KEY == key.F3:
            self.show_info = not self.show_info

    def on_key_release(self, KEY, MOD):
        if KEY in (key.W, key.S):
            self.camera.set_move_vertical(0)
        elif KEY in (key.A, key.D):
            self.camera.set_move_horizontal(0)

    def on_resize(self, width, height):
        self.init_gl(width, height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.camera.mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, x, y, dx, dy):
        self.camera.mouse_scroll(x, y, dx, dy, self.width, self.height)

    def on_draw(self):
        self.init_2d()

        self.camera.draw()

        self.grid.draw()
        self.gob.draw()

        self.panel.draw()
        if self.show_info:
            self.fps_display.draw()
            self.zoom_level.draw()

        # Remove default modelview matrix
        glPopMatrix()

    def run(self):
        pyglet.app.run()

    def init_2d(self):
        # Initialize Projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Initialize Modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Save the default modelview matrix
        glPushMatrix()

        # Clear window with ClearColor
        glClear(GL_COLOR_BUFFER_BIT)

    def init_gl(self, width, height):
        # Set antialiasing
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        # Set alpha blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Set viewport
        glViewport(0, 0, width, height)

    def window_settings(self):
        # self.set_minimum_size(200, 200)
        self.set_location(400, 200)
