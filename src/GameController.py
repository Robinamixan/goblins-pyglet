from src.GameElements.Mobs.MobsController import MobsController
import copy


class GameController:
    def __init__(self):
        self.mobs_group = []
        self.static_objects = []
        self.focused = None
        self.mob_controller = MobsController(self)

    def set_focus(self, mouse_position):
        focus = None
        for mob in self.mobs_group:
            if mob.is_inside(mouse_position):
                focus = mob
                break
        self.focused = focus

    def get_focused(self):
        return self.focused

    def add_mob(self, mob_object):
        self.mobs_group.append(mob_object)

    def remove_mob(self, mob_object):
        self.mobs_group.remove(mob_object)

        if self.focused == mob_object:
            self.focused = None

    def update_mobs(self, dt):
        group = copy.copy(self.mobs_group)
        for mob in self.mobs_group:
            if not mob.check_collision(self.get_object_around(mob, 50, group)):
                mob.update(dt)

    def get_object_around(self, mob_current, radius, group):
        objects = []
        point = mob_current.get_position()
        start_x = point[0] - radius
        start_y = point[1] - radius

        end_x = point[0] + radius
        end_y = point[1] + radius

        for mob in group:
            if mob == mob_current:
                continue
            position = mob.get_position()
            hor = start_x <= position[0] <= end_x
            vert = start_y <= position[1] <= end_y
            if hor and vert:
                objects.append(mob)

        return objects

    def draw_mobs(self):
        for mob in self.mobs_group:
            mob.draw()

    def create_gob(self, name, position):
        self.add_mob(self.mob_controller.create_gob(name, position))
