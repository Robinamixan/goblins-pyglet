from src.GameElements.Mobs.Mob import MobClass
from src.Constants import *


class MobsController:
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def create_gob(self, name, position, batch):
        return MobClass(self.game_controller, batch, name, position, (1, 1), 10, 2, goblin_image_front)

    def is_mob(self, game_object):
        return isinstance(game_object, MobClass)
