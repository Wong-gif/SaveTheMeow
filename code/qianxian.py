import pygame
from sys import exit

window_width, window_height = 1280, 720
tile_size = 128

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width,window_height))
        pygame.display.set_caption("Save The Meow")

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