import pygame
from qx_farm_settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load("graphics_qx/test/rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load("graphics_qx/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)