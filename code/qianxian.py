import pygame
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join

window_width, window_height = 1280, 720
tile_size = 128

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width,window_height))
        pygame.display.set_caption("Save The Meow")

        self.all_sprites = pygame.sprite.Group()

        self.import_map()
        self.setup(self.tmx_maps["world"],"(0)")

    def import_map(self):
        self.tmx_maps = {"world": load_pygame(join("Tiled (data) qianxian", "tmx", "2d world map.tmx"))}

    def setup(self, tmx_map,player_start_pos):
        for x,y,surf in tmx_map.get_layer_by_name("Floor").tiles():
         Sprite((x*tile_size,y*tile_size),surf,self.all_sprites)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

game = Game()
game.run()