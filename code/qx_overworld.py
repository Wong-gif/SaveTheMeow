from qx_settings import *
from qx_sprites import Sprite

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data 

        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_map,overworld_frames)

    def setup(tmx_map,overworld_frames):
        #layers
        for layer in ["main","top"]:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
            Sprite()

    def run(self,dt):
        pass