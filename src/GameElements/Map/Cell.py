class CellClass:
    passable = True
    contain = []
    x = 0
    y = 0
    size = 0

    def __init__(self, x, y, size):
        self.passable = True
        self.contain = []
        self.x = x
        self.y = y
        self.size = size

    def is_empty(self):
        return not self.contain

    def is_passable(self):
        return self.passable

    def is_can_move(self, moved_object):
        if self.is_passable():
            return True
        else:
            if moved_object == self.contain:
                return True
            else:
                return False

    def get_object(self):
        if self.contain:
            return self.contain[-1]
        else:
            return False

    def set_object(self, map_object, passable=False):
        self.contain.append(map_object)
        if not passable:
            self.passable = False

    def remove_object(self, map_object):
        self.contain.remove(map_object)
        if not map_object.passable:
            self.passable = True
