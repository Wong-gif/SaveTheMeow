from qx_settings import *
from pytmx.util_pygame import load_pygame
from os.path import join
from qx_overworld import Overworld
from qx_support import * 

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width,window_height))
        pygame.display.set_caption("Save The Meow")
        self.clock = pygame.time.Clock()
        self.import_assets()

        #generate the world map
        self.tmx_overworld = load_pygame(join("tiled_data_qianxian","tmx","overworld.tmx"))
        self.current_stage = Overworld(self.tmx_overworld,self.overworld_frames)

    def import_assets(self):
        self.overworld_frames = {
            "palms" : import_folder("graphics_qx","overworld","palm"),
            "water" : import_folder("graphics_qx","overworld","water"),
            "path" : import_folder_dict("graphics_qx","overworld","path"),
            "icon" : import_sub_folders("graphics_qx","overworld","icon")
        }

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.current_stage.run(dt)
            pygame.display.update()

game = Game()
game.run()