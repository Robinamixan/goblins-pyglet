from src.GameElements.GameObject import GameObject


class WallClass(GameObject):
    def __init__(self, game_controller, batch, name, point, size, image_path):
        super().__init__(game_controller, batch, name, point, size, image_path)
