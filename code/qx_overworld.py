from qx_settings import *

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data 

        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_map,overworld_frames)

    def setup(tmx_map,overworld_frames):
        pass