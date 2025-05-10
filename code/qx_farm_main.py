import pygame, sys
from qx_farm_settings import *

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT():
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            pygame.display.update()
            self.clock.tick(FPS)

game = Game()
game.run()