import pyglet


class MobClass:
    def __init__(self, name, position):
        self.name = name
        self.x = position[0]
        self.y = position[1]
        self.width = 25
        self.height = 25
        image = pyglet.image.load('../resources/goblin_alpha_1.1.png')
        self.sprite = pyglet.sprite.Sprite(image, x=self.x, y=self.y)
        self.sprite.image.width = 25
        self.sprite.image.height = 25

        self.vector_y = 10

    def get_position(self):
        return self.sprite.position

    def get_size(self):
        return self.width, self.height

    def get_name(self):
        return self.name

    def distance_q(self, target):
        return (self.x - target.x) ** 2 + (self.y - target.y) ** 2

    def is_inside(self, point):
        horizontal = self.x <= point[0] <= self.x + self.width
        vertical = self.y <= point[1] <= self.y + self.height

        return horizontal and vertical

    def check_collision(self, mobs_group):
        if self in mobs_group:
            mobs_group.remove(self)
        for mob in mobs_group:
            if self.distance_q(mob) < (self.width / 2 + mob.width / 2)**2:
                return True

    def set_vector_x(self):
        self.vector_y = -self.vector_y

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.y += dt*self.vector_y
        self.y = self.sprite.y

    def get_next_position(self, dt):
        next_x = self.sprite.x + dt *self.vector_y
