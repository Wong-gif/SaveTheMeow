from qx_settings import *
from qx_sprites import Sprite, AnimatedSprite, Node, Icon
from qx_groups import WorldSprites
from  random import randint

class Overworld:
    def __init__(self, tmx_map,data, overworld_frames):
        self.display_surface = pygame.display.get_surface() 
        self.data = data

        self.all_sprites = WorldSprites(data)

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

        #path
        self.paths = {}
        for obj in tmx_map.get_layer_by_name("Paths"):
          pos = [int((p.x + tile_size/2),(p.y + tile_size/2)) for p in obj.points]
          start = obj.properties["start"]
          end = obj.properties["end"]
          self.paths[end] = {"pos":pos, "start":start}

        #nodes & player
        for obj in tmx_map.get_layer_by_name("Nodes"):
         #player
         if obj.name == "Node" and int(obj.properties["stage"]) == self.data.current_level:
          self.icon = Icon((obj.x + tile_size/2, obj.y + tile_size/2), self.all_sprites, overworld_frames["icon"])
         
         #nodes
         if obj.name == "Node":
          Node( pos = (obj.x,obj.y),
               surf = overworld_frames["path"]["node"],
               groups = self.all_sprites,
               level = int(obj.properties["stage"]),
               data = self.data)

    def run(self,dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.icon.rect.center)