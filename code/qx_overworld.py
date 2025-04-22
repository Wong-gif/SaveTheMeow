from qx_settings import *
from qx_sprites import Sprite, AnimatedSprite
from qx_groups import WorldSprites
from  random import randint

class Overworld:
    def __init__(self, tmx_map, overworld_frames):
        self.display_surface = pygame.display.get_surface() 

        self.all_sprites = WorldSprites()

        self.setup(tmx_map,overworld_frames)

    def setup(self,tmx_map,overworld_frames):
        #layers
        for layer in ["main","top"]:
         for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
          Sprite((x*tile_size,y*tile_size), surf, self.all_sprites, Z_layers["bg tiles"])

        #water
        for col in range(tmx_map.width):
           for row in range(tmx_map.height):
              AnimatedSprite((col*tile_size,row*tile_size), overworld_frames["water"],self.all_sprites,Z_layers["bg"])

        #objects
        for obj in tmx_map.get_layer_by_name("Objects"):
         if obj.name == "palm":
            AnimatedSprite((obj.x,obj.y),overworld_frames["palms"],self.all_sprites,Z_layers["main"],randint(4,6))
         else:
            z = Z_layers[f"{"bg details" if obj.name == "grass" else "bg tiles"}"]
            Sprite((obj.x,obj.y), obj.image, self.all_sprites, z)

    def run(self,dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw((1500,900))