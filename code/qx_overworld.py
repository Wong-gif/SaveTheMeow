from qx_settings import *
from qx_sprites import Sprite, AnimatedSprite, Node, Icon, PathSprite
from qx_groups import WorldSprites
from qx_entites import Character, DialogManager
from  random import randint
from jh_test_main import platform_map
from ken_boss_test import boss_battle
from ken_weapon_market_test import open_store

class Overworld:
    def __init__(self, tmx_map,data, overworld_frames):
        self.display_surface = pygame.display.get_surface() 
        self.data = data

        self.all_sprites = WorldSprites(data)
        self.node_sprites = pygame.sprite.Group()

        self.setup(tmx_map,overworld_frames)

        self.current_node = [node for node in self.node_sprites if node.level == 0][0]

        self.path_frames = overworld_frames["path"]
        self.create_path_sprites()

        self.dialog_active = False
        self.dialog_manager = DialogManager()
        self.font = pygame.font.Font(None,36)

        self.nearby_character = None

        self.dialogue_finished = False

        self.space_pressed = False

        self.open_store = open_store
        self.platform_map = platform_map
        self.boss_battle = boss_battle

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
          
        self.characters = []

        for obj in tmx_map.get_layer_by_name("Entities"):
          if obj.name == "Character":
            character = Character(
              pos = (obj.x, obj.y),
              frames = overworld_frames["characters"][obj.properties["graphic"]],
              groups = self.all_sprites,
              facing_direction = obj.properties["direction"],
              action = self.define_npc_action(obj.properties.get("character_id","default")))
            
            if "dialog" in obj.properties:
              dialog_text = obj.properties["dialog"].split("|")
              character.dialog_manager.set_dialogue(dialog_text)
              character.dialog_text = dialog_text

            self.characters.append(character)

        #path
        self.paths = {}
        for obj in tmx_map.get_layer_by_name("Paths"):
          pos = [(int(p.x + tile_size/2),int(p.y + tile_size/2)) for p in obj.points]
          start = int(obj.properties["start"])
          end = int(obj.properties["end"])
          self.paths[end] = {"pos" : pos, "start" : start}

        #nodes & player
        for obj in tmx_map.get_layer_by_name("Nodes"):
         #player
         if obj.name == "Node" and int(obj.properties["stage"]) == self.data.current_level:
          self.icon = Icon((obj.x + tile_size/2, obj.y + tile_size/2), self.all_sprites, overworld_frames["icon"])
         
         #nodes
         if obj.name == "Node":
          available_paths = {k:v for k,v in obj.properties.items() if k in("left","right","up","down")}

          Node( pos = (obj.x,obj.y),
               surf = overworld_frames["path"]["node"],
               groups = (self.all_sprites,self.node_sprites),
               level = int(obj.properties["stage"]),
               data = self.data,
               paths = available_paths)
          
    def check_dialogue(self):
      self.nearby_character = None

    # Get the player's icon rect (center only, no direction yet)
      icon_rect = self.icon.rect

    # Define a proximity box around the player's center (adjust size for proximity)
      check_rect = pygame.Rect(icon_rect.center[0] - 40, icon_rect.center[1] - 40, 80, 80)  # Larger area for testing

    # Loop through characters and check if any NPC is within the proximity box
      for character in self.characters:
        if check_rect.colliderect(character.rect):  # Use colliderect for proximity checking
            if not self.dialog_active:
             self.nearby_character = character
            break
          
    def define_npc_action(self,character_id):
      if character_id == "o2":
        return open_store
      elif character_id == "o3":
        return boss_battle
      elif character_id == "o4":
        return platform_map
      elif character_id == "o5":
        return boss_battle
      else :
        return None

    def create_path_sprites(self):
      #get tiles from path
      nodes = {node.level: vector(node.grid_pos) for node in self.node_sprites}
      path_tiles = {}

      for path_id, data in self.paths.items():
        path = data["pos"]
        start_node, end_node = nodes[data["start"]], nodes[path_id]
        path_tiles[path_id] = [start_node]

        for index, points in enumerate(path):
          if index < len(path) - 1:
            start,end = vector(points), vector(path[index + 1])
            path_dir = (end - start) / tile_size
            start_tile = vector(int(start[0]/tile_size), int(start[1]/tile_size))

            if path_dir.y:
              dir_y = 1 if path_dir.y > 0 else -1
              for y in range(dir_y, int(path_dir.y) + dir_y, dir_y):
                path_tiles[path_id].append(start_tile + vector(0,y))

            if path_dir.x:
              dir_x  = 1 if path_dir.x > 0 else -1
              for x in range(dir_x, int(path_dir.x) + dir_x, dir_x):
                path_tiles[path_id].append(start_tile + vector(x,0))

        path_tiles[path_id].append(end_node)

      #create sprites
      for key, path in path_tiles.items():
        for index,tile in enumerate(path):
            if index > 0 and index < len(path) - 1:
              prev_tile = path[index - 1] - tile
              next_tile = path[index + 1] - tile

              if prev_tile.x == next_tile.x:
                surf = self.path_frames["vertical"]
              elif prev_tile.y == next_tile.y:
                surf = self.path_frames["horizontal"]
              else:
                if prev_tile.x == -1 and next_tile.y == -1 or prev_tile.y == -1 and next_tile.x == -1:
                  surf = self.path_frames["tl"]
                elif prev_tile.x == 1 and next_tile.y == 1 or prev_tile.y ==1 and next_tile.x == 1:
                  surf = self.path_frames["br"]
                elif prev_tile.x == -1 and next_tile.y == 1 or prev_tile.y == 1 and next_tile.x == -1:
                  surf = self.path_frames["bl"]
                elif prev_tile.x == 1 and next_tile.y == -1 or prev_tile.y == -1 and next_tile.x == 1:
                  surf = self.path_frames["tr"]
                else:
                  surf = self.path_frames["horizontal"]


              PathSprite(
               pos = (tile.x * tile_size, tile.y * tile_size), 
               surf = surf,
               groups = self.all_sprites,
               level = key)
          
    def input(self):
      keys = pygame.key.get_pressed()

      if keys[pygame.K_SPACE]:
            if not self.space_pressed:  # Only trigger if space hasn't been processed yet
                self.space_pressed = True  # Mark space as pressed

                if self.dialog_active:
                    if self.dialog_manager.has_more_line():
                      self.dialog_manager.next_line()
                    else:
                     self.dialog_active = False
                     self.dialogue_finished = True
                     self.nearby_character = None
                elif self.nearby_character and not self.dialog_active:
                  self.dialog_manager.set_dialogue(self.nearby_character.dialog_text)
                  self.dialog_active = True
                  self.dialogue_finished = False
      else:
            self.space_pressed = False  # Reset the flag when spacebar is released

      if keys[pygame.K_RETURN] and self.dialog_active and not self.dialog_manager.has_more_line():
        if not hasattr(self,"enter_pressed"):
          self.enter_pressed = False

        if not self.enter_pressed and self.dialog_active and not self.dialog_manager.has_more_line():
          self.enter_pressed = True
          print("Dialogue has finished")
          if self.nearby_character and self.nearby_character.action:
            self.nearby_character.action()

          self.dialogue_finished = False
          self.nearby_character = None

      else :
        self.enter_pressed = False

      if self.current_node and not self.icon.path and not self.dialog_active:
        if keys[pygame.K_DOWN] and self.current_node.can_move("down"):
          self.move("down")
        if keys[pygame.K_LEFT] and self.current_node.can_move("left"):
          self.move("left")
        if keys[pygame.K_RIGHT] and self.current_node.can_move("right"):
          self.move("right")
        if keys[pygame.K_UP] and self.current_node.can_move("up"):
          self.move("up")

    def move(self,direction):
      path_key = int(self.current_node.paths[direction][0])
      path_reverse = True if self.current_node.paths[direction][-1] == "r" else False
      path = self.paths[path_key]["pos"][:] if not path_reverse else self.paths[path_key]["pos"][::-1]
      self.icon.start_move(path)

    def get_current_node(self):
      nodes = pygame.sprite.spritecollide(self.icon, self.node_sprites, False)
      if nodes:
        self.current_node = nodes[0]

    def draw_dialog(self):
      if self.dialog_active and self.dialog_manager.get_current_line():
        box_rect = pygame.Rect(50, window_height - 150, window_width - 100, 100)
        pygame.draw.rect(self.display_surface, (0, 0, 0), box_rect)
        pygame.draw.rect(self.display_surface, (255, 255, 255), box_rect, 3)

        text_surf = self.font.render(self.dialog_manager.get_current_line(), True, (255, 255, 255))
        self.display_surface.blit(text_surf, (box_rect.x + 20, box_rect.y + 30))

    def run(self,dt):
        self.input()
        self.get_current_node()
        if not self.dialog_active:
          self.check_dialogue()
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.icon.rect.center)

        if self.dialog_active:
          self.draw_dialog()