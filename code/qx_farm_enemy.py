import pygame
from qx_farm_settings import *
from qx_farm_entity import Entity
from qx_support import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups):
        #general setup
        super().__init__(groups)
        self.sprite_type = "enemy"

        #graphics 
        self.import_graphics(monster_name)
        self.status  = "idle"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

    def import_graphics(self,name):
        self.animations = {"idle":[],"move":[],"attack":[]}
        main_path = f"graphics_qx/monsters_farming/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder_farm(main_path + animation)