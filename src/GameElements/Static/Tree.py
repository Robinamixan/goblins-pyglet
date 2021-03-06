from src.GameElements.GameObject import GameObject


class TreeClass(GameObject):
    def __init__(self, game_controller, batch, name, point, size, image_path):
        super().__init__(game_controller, batch, name, point, size, image_path)

    def update(self, dt):
        self.game_controller.generate_items_around(self.point, speed=10)
