from src.GameElements.Mobs.MobClass import MobClass


class MobsController:
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def create_gob(self, name, position):
        return MobClass(name, position)
