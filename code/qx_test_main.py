def open_game(username):
    import pygame
    from qx_settings import window_height,window_width,Z_layers,animation_speed
    from pytmx.util_pygame import load_pygame
    from os.path import join
    from qx_overworld import Overworld
    from qx_support import import_folder,import_folder_dict,import_sub_folders,all_character_import
    from qx_data import Data

    class Game:
        def __init__(self, username):
            self.username = username
            self.running = True  # Add a running flag
            self.init_game()
            
        def init_game(self):
            pygame.init()
            self.display_surface = pygame.display.set_mode((window_width,window_height))
            pygame.display.set_caption("Save The Meow")
            self.clock = pygame.time.Clock()
            self.import_assets()
            self.data = Data()
            self.tmx_overworld = load_pygame(join("tiled_data_qianxian","tmx","overworld.tmx"))
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.username)

        def import_assets(self):
            self.overworld_frames = {
                "palms": import_folder("graphics_qx","overworld","palm"),
                "water": import_folder("graphics_qx","overworld","water"),
                "path": import_folder_dict("graphics_qx","overworld","path"),
                "icon": import_sub_folders("graphics_qx","overworld1","icon"),
                "characters": all_character_import("graphics_qx","characters")
            }

        def run(self):
            while self.running:
                dt = self.clock.tick() / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game()
                        return  # Exit the run loop

                self.current_stage.run(dt)
                pygame.display.update()
                
        def quit_game(self):
            self.running = False
            pygame.quit()

    game = Game(username)
    game.run()