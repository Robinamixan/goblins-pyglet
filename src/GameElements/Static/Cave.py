from src.GameElements.GameObject import GameObject
from src.GameElements.Inventory.Staff import StaffClass
from src.GameElements.Inventory.Inventory import InventoryClass


class CaveClass(GameObject):
    def __init__(self, game_controller, batch, name, point, size, image_path):
        super().__init__(game_controller, batch, name, point, size, image_path)

        self.staff = StaffClass(4)
        self.inventory = InventoryClass(10)
        self.around_points = self.get_around_points()
        self.targets = []

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
            point = [self.point[0] + 1, self.point[1] - 1]
            self.show_member(member, point)

            return member

    def show_member(self, member, point):
        member.set_visible(True)
        member.set_point(point)
        if self.game_controller.is_mob(member):
            member.set_destination(point)

        self.staff.get_out(member.get_name())
        self.game_controller.add_object_in_cell(point, member)

    def hide_member(self, member):
        member.set_visible(False)
        self.staff.get_in(member.get_name())
        self.game_controller.remove_object_from_cell(member.get_point(), member)

    def go_back(self, member):
        point = [self.point[0] + 1, self.point[1] - 1]
        member.set_target(point)
        member.set_action('return')

    def gather_food(self, member):
        food = self.game_controller.get_food_item(member.get_point(), excepts=self.targets)
        if food:
            point = food.get_point()
            self.targets.append(point)
            member.set_target(point)

    def get_resources(self, member):
        for index, item in member.get_inventory_info()['items'].items():
            if item['object']:
                self.inventory.add_items(item['object'], item['amount'])
                member.remove_items(item['object'], item['amount'])

    def take_in(self, member):
        self.hide_member(member)
        self.get_resources(member)

    def update(self, dt):
        self.manage_staff_outside()
        self.manage_staff_inside()

    def manage_staff_outside(self):
        members = self.staff.get_all_outside()
        for member in members:
            if member.is_waiting():
                self.check_target(member.get_point())
                if member.get_point() in self.around_points:
                    self.take_in(member)
                    continue
                if member.is_inventory_full():
                    self.go_back(member)
                    continue

                self.gather_food(member)

    def manage_staff_inside(self):
        food = self.game_controller.get_food_item(excepts=self.targets)
        if food and not self.inventory.is_full():
            member = self.send_member()
            if member:
                self.gather_food(member)

    def get_staff_info(self):
        return {
            'members': self.staff.get_all_staff(),
            'size': self.staff.get_size()
        }

    def check_target(self, point):
        if point in self.targets:
            self.targets.remove(point)

    def get_inventory_info(self):
        return self.inventory.get_info()
