import pyglet


class MobClass:
    def __init__(self, x=0, y=0):
        image = pyglet.image.load('../resources/goblin_alpha_1.1.png')
        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y)

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.x += dt
