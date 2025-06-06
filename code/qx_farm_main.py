import pygame, sys
from qx_farm_settings import *
from qx_farm_level import Level

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption("Farming Map")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(WATER_COLOUR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

game = Game()
game.run()