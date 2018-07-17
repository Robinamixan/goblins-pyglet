from src.GameElements.GameObject import GameObject


class ItemClass(GameObject):
    def __init__(self, game_controller, batch, name, point, size, image_path):
        super().__init__(game_controller, batch, name, point, size, image_path)

        self.edible = False
        self.passable = True
        self.satiety = 0
        self.stack = 4

    def set_edible(self, edible):
        self.edible = edible

    def get_edible(self):
        return self.edible
