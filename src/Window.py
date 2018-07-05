import pyglet


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(200, 200)
        self.set_location(400, 200)
        self.frame_rate = 1 / 60.0

    def on_draw(self):
        self.clear()

    def update(self, dt):
        pass
