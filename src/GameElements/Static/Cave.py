from src.GameElements.GameObject import GameObject
from src.GameElements.Inventory.Staff import StaffClass


class CaveClass(GameObject):
    def __init__(self, game_controller, batch, name, point, size, image_path):
        super().__init__(game_controller, batch, name, point, size, image_path)

        self.staff = StaffClass(4)

    def add_to_staff(self, mob):
        self.staff.add_to_staff(mob)
        mob.set_visible(False)

    def remove_from_staff(self, mob):
        self.staff.remove_mob(mob)

    def send_member(self):
        member = self.staff.get_mob()

        if member:
            member.set_visible(True)

            point = (self.point[0] + 1, self.point[1] - 1)
            member.set_point(point)

            if self.game_controller.is_mob(member):
                member.set_destination(point)
            self.staff.get_out(member.get_name())
            self.game_controller.add_object_in_cell(point, member)

    def get_staff_info(self):
        return {
            'members': self.staff.get_all_staff(),
            'size': self.staff.get_size()
        }
