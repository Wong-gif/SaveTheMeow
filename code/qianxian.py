import pygame
from sys import exit
from pytmx.util_pygame import load_pygame

window_width, window_height = 1280, 720
tile_size = 128

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width,window_height))
        pygame.display.set_caption("Save The Meow")

    def import_map(self):
        self.tmx_maps = {"world": load_pygame("Tiled (data) qianxian/tmx/2d world map.tmx")}

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