import pygame
from qx_farm_settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surf = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surf
        if sprite_type == "object":
            #offset for objects only as their images are larger
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)