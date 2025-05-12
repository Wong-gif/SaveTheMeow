import pygame
from qx_farm_settings import *
from qx_farm_player import Player
from qx_farm_tile import Tile
from qx_support import *
from random import choice

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
        layout = {
            "boundary" : import_csv_layout("farm_map/farming_map_FloorBlocks.csv"),
            "grass" : import_csv_layout("farm_map/farming_map_Grass.csv"),
            "object" : import_csv_layout("farm_map/farming_map_Objects.csv")
        }
        
        graphics = {
            "grass" : import_folder_farm("graphics_qx/grass"),
            "objects" : import_folder_farm("graphics_qx/objects")
        }

        for style,layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x,y),[self.obstacles_sprites],"invisible")
                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"grass",random_grass_image)
                        
                       # if style == "object":
                        #    surf = graphics['objects'][int(col)]
                         #   Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"object",surf)
        self.player = Player((1800,1600),[self.visible_sprites],self.obstacles_sprites)

    def run(self):
        #update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group): #craetes a camera that follows the player and has overlapping effect
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load("graphics_qx/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)