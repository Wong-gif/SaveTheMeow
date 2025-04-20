from qx_settings import *
from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width,window_height))
        pygame.display.set_caption("Save The Meow")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            print(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

game = Game()
game.run()