import pygame
from qx_farm_settings import *
from qx_farm_groups import Tile, Player

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #sprite
        self.create_map()

    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == "x":
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
                if col == "p":
                    self.player = Player((x,y),[self.visible_sprites],self.obstacles_sprites)

    def run(self):
        #update and draw game
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group): #craetes a camera that follows the player and has overlapping effect
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image,sprite.rect)