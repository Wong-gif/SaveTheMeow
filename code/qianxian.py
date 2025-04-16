import pygame
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join

window_width, window_height = 1280, 720
tile_size = 128

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width,window_height))
        pygame.display.set_caption("Save The Meow")

        self.import_map()
        self.setup(self.tmx_maps["world"],"")

    def import_map(self):
        self.tmx_maps = {"world": load_pygame(join("Tiled (data) qianxian", "tmx", "2d world map.tmx"))}

    def setup(self, tmx_map, player_start_pos):
        for x,y,surf in tmx_map.get_layer_by_name("Floor").tiles():
         print(x,y,surf)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()