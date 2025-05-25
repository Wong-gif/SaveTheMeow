import pygame
from qx_farm_settings import *
from qx_farm_entity import Entity
from qx_support import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites):
        #general setup
        super().__init__(groups)
        self.sprite_type = "enemy"

        #graphics 
        self.import_graphics(monster_name)
        self.status  = "idle"
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.atack_type = monster_info["attack_type"]


    def import_graphics(self,name):
        self.animations = {"idle":[],"move":[],"attack":[]}
        main_path = f"graphics_qx/monsters_farming/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder_farm(main_path + animation)

    def update(self):
        self.move(self.speed)