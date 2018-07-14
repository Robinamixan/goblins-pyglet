class StaffClass:
    def __init__(self, size):
        self.size = size
        self.staff = {}

    def get_size(self):
        return self.size

    def add_to_staff(self, mob, inside=True):
        name = mob.get_name()
        self.staff[name] = {}
        self.staff[name]['mob'] = mob
        self.staff[name]['inside'] = inside

    def remove_mob(self, mob):
        for name, member in self.staff.items():
            if member == mob:
                del self.staff[name]

    def get_mob(self, name='', is_inside=True):
        if name == '':
            for name, member in self.staff.items():
                if is_inside:
                    if member['inside']:
                        return member['mob']
                else:
                    return member['mob']
        else:
            return self.staff[name]['mob']

    def get_all_staff(self):
        return self.staff

    def get_out(self, name):
        self.staff[name]['inside'] = False

    def get_in(self, name):
        self.staff[name]['inside'] = True

    def get_all_outside(self):
        members = []
        for name, member in self.staff.items():
            if not member['inside']:
                members.append(member['mob'])

        return members

