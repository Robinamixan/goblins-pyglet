from src.GameElements.GameObject import GameObject
from src.GameElements.Inventory.Staff import StaffClass


class CaveClass(GameObject):
    def __init__(self, game_controller, batch, name, point, size, image_path):
        super().__init__(game_controller, batch, name, point, size, image_path)

        self.staff = StaffClass(4)

        gob = self.game_controller.create_gob('test_1', point, add_to_cell=False)
        self.add_to_staff(gob)

        gob = self.game_controller.create_gob('test_2', point, add_to_cell=False)
        self.add_to_staff(gob)

    def add_to_staff(self, mob):
        self.staff.add_to_staff(mob)
        mob.set_visible(False)

    def remove_from_staff(self, mob):
        self.staff.remove_member(mob)

    def send_member(self):
        member = self.staff.get_member()

        if member:
            member.set_visible(True)

            point = (self.point[0] + 1, self.point[1] - 1)
            member.set_point(point)

            if self.game_controller.is_mob(member):
                member.set_destination(point)
            self.staff.get_out(member.get_name())
            self.game_controller.add_object_in_cell(point, member)

            destin_point = [self.point[0] + 5, self.point[1] - 5]
            member.set_target(destin_point)

    def get_back(self, member):
        point = [self.point[0] + 1, self.point[1] - 1]
        member.set_target(point)
        member.set_action('return')

    def get_inside(self, member):
        member.set_visible(False)
        self.staff.get_in(member.get_name())
        self.game_controller.remove_object_from_cell(member.get_point(), member)

    def update(self, dt):
        members = self.staff.get_all_outside()
        for member in members:
            if member.is_waiting():
                if member.is_inventory_full():
                    self.get_back(member)

                if member.get_point() in self.get_around_points():
                    self.get_inside(member)

    def get_staff_info(self):
        return {
            'members': self.staff.get_all_staff(),
            'size': self.staff.get_size()
        }
