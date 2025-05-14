from qx_settings import * #import all the constants from settings
from qx_sprites import Sprite, AnimatedSprite, Node, Icon, PathSprite
from qx_groups import WorldSprites
from qx_entites import Character, DialogManager
from  random import randint
from jh_test_main import platform_map #import function to start platform level
from ken_boss_test import boss_battle #import function to start boss level
from ken_weapon_market_test import open_store #import function to open the store
from qx_test_farm import farming_map

class Overworld: #creates the overworld class
    def __init__(self, tmx_map,data, overworld_frames): #initializes overworld with map, data, and sprite frames
        self.display_surface = pygame.display.get_surface() ## Gets main display surface to render
        self.data = data #stores reference to game data object

        self.all_sprites = WorldSprites(data)
        self.node_sprites = pygame.sprite.Group() #creates group for just node sprites

        self.setup(tmx_map,overworld_frames) #calls setup to place tiles, paths, characters and objects

        self.current_node = [node for node in self.node_sprites if node.level == 0][0] #finds node for stage 0

        self.path_frames = overworld_frames["path"] #loads path tile images from provided frames
        self.create_path_sprites() #creates the actual path tiles on the map

        self.dialog_active = False #flag for whether a dialogue is currently showing
        self.dialog_manager = DialogManager() #initializes dialog manager
        self.font = pygame.font.Font(None,36) #sets font for text display

        self.nearby_character = None #keeps track of the npc that the player is near

        self.dialogue_finished = False  #tracks if the current dialogue is completed

        self.space_pressed = False #used to prevent space key from getting too many inputs from just one press

        self.open_store = open_store #assign store function to a variable
        self.platform_map = platform_map #assign platform map to a variable
        self.boss_battle = boss_battle #assign boss battle to a variable
        self.farming_map = farming_map

    def setup(self,tmx_map,overworld_frames): #sets up tiles, paths, and characters from tmc map
        #layers
        for layer in ["main","top"]: #loops through tile layers
         for x, y, surf in tmx_map.get_layer_by_name(layer).tiles(): #loops through each tile in layer
          Sprite((x*tile_size,y*tile_size), surf, self.all_sprites, Z_layers["bg tiles"]) #adds each tile as sprite

        #water
        for col in range(tmx_map.width): #loops through map columns
           for row in range(tmx_map.height): #loops through map rows
              AnimatedSprite((col*tile_size,row*tile_size), overworld_frames["water"],self.all_sprites,Z_layers["bg"]) #adds animated water

        #objects
        for obj in tmx_map.get_layer_by_name("Objects"): #loops through object layer
         if obj.name == "palm": #if the ojects has the name of palm
            AnimatedSprite((obj.x,obj.y),overworld_frames["palms"],self.all_sprites,Z_layers["main"],randint(4,6)) #add animated palm with random speed
         else: #for all other objects
            z = Z_layers[f"{"bg details" if obj.name == "grass" else "bg tiles"}"] #determine its layer depth based on its name and assign it according it z layers value
            Sprite((obj.x,obj.y), obj.image, self.all_sprites, z) #add static object sprite
          
        self.characters = []  #list to store character objects

        for obj in tmx_map.get_layer_by_name("Entities"): #loop through entities layer, made for npc
          if obj.name == "Character": #if the name is a character object
            character = Character( #create character object
              pos = (obj.x, obj.y),
              frames = overworld_frames["characters"][obj.properties["graphic"]],
              groups = self.all_sprites,
              facing_direction = obj.properties["direction"],
              action = self.define_npc_action(obj.properties.get("character_id","default")))
            
            if "dialog" in obj.properties: #if character has dialog property
              dialog_text = obj.properties["dialog"].split("|") # split dialog into lines bsaed on the | symbol
              character.dialog_manager.set_dialogue(dialog_text) #assign dialogue to character
              character.dialog_text = dialog_text #store dialogue lines on character

            self.characters.append(character) # add that character to the list

        #path
        self.paths = {} # dictionary to store path info
        for obj in tmx_map.get_layer_by_name("Paths"): #loop through paths layer
          pos = [(int(p.x + tile_size/2),int(p.y + tile_size/2)) for p in obj.points] #get center positions of path points
          start = int(obj.properties["start"]) #get start node index
          end = int(obj.properties["end"]) #get end node index
          self.paths[end] = {"pos" : pos, "start" : start} #store path data

        #nodes & player
        for obj in tmx_map.get_layer_by_name("Nodes"): #loop through Nodes layer
         #player
         if obj.name == "Node" and int(obj.properties["stage"]) == self.data.current_level: #if node is current level
          self.icon = Icon((obj.x + tile_size/2, obj.y + tile_size/2), self.all_sprites, overworld_frames["icon"]) #add icon at that node
         
         #nodes
         if obj.name == "Node": #Ffor all nodes
          available_paths = {k:v for k,v in obj.properties.items() if k in("left","right","up","down")} #get path directions

          Node( pos = (obj.x,obj.y), #create Node object
               surf = overworld_frames["path"]["node"],
               groups = (self.all_sprites,self.node_sprites),
               level = int(obj.properties["stage"]),
               data = self.data,
               paths = available_paths)
          
    def check_dialogue(self): #to check if icon is close to any npc character
      self.nearby_character = None #reset nearby npc character

      icon_rect = self.icon.rect #get icon's rectangle

    #define a proximity box around the player's center (adjust size for proximity)
      check_rect = pygame.Rect(icon_rect.center[0] - 40, icon_rect.center[1] - 40, 80, 80)  #larger area for testing

    #loop through characters and check if any npc is within the proximity box
      for character in self.characters: #loop through npc characters
        if check_rect.colliderect(character.rect):  #use colliderect for proximity checking
            if not self.dialog_active: #if no dialogue showing
             self.nearby_character = character #set current nearby character
            break #stop checking once one character is found
          
    def define_npc_action(self,character_id): #returns function to call based on character id
      if character_id == "o2":
        return open_store
      elif character_id == "o3":
        return platform_map
      elif character_id == "o4":
        return farming_map
      elif character_id == "o5":
        return boss_battle
      else :
        return None #return nothing fif it doesnt have an id

    def create_path_sprites(self): #creates tiles for visual paths
      #get tiles from path
      nodes = {node.level: vector(node.grid_pos) for node in self.node_sprites} #get node grid positions
      path_tiles = {} #stores tiles for each path

      for path_id, data in self.paths.items(): #loop through paths
        path = data["pos"] #get a list of points
        start_node, end_node = nodes[data["start"]], nodes[path_id]  #get start and end nodes
        path_tiles[path_id] = [start_node] #start path list

        for index, points in enumerate(path): #loop through path points
          if index < len(path) - 1: #skips the last point
            start,end = vector(points), vector(path[index + 1]) #get a pair of point
            path_dir = (end - start) / tile_size #get direction
            start_tile = vector(int(start[0]/tile_size), int(start[1]/tile_size)) #tile coordinate

            if path_dir.y: #if the path is vertical
              dir_y = 1 if path_dir.y > 0 else -1
              for y in range(dir_y, int(path_dir.y) + dir_y, dir_y):
                path_tiles[path_id].append(start_tile + vector(0,y)) #add vertical steps

            if path_dir.x: #if path is horizontal
              dir_x  = 1 if path_dir.x > 0 else -1
              for x in range(dir_x, int(path_dir.x) + dir_x, dir_x):
                path_tiles[path_id].append(start_tile + vector(x,0)) #add horizontal steps

        path_tiles[path_id].append(end_node) #add end tile

      #create sprites
      for key, path in path_tiles.items(): #loop through each path
        for index,tile in enumerate(path): #loop through tiles
            if index > 0 and index < len(path) - 1: #skip endpoints
              prev_tile = path[index - 1] - tile #get the direction from previous tile
              next_tile = path[index + 1] - tile #get the direction to next tile

              if prev_tile.x == next_tile.x:
                surf = self.path_frames["vertical"] #use vertical tile
              elif prev_tile.y == next_tile.y:
                surf = self.path_frames["horizontal"] #use horizontal tile
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
                  surf = self.path_frames["horizontal"] #fallback


              PathSprite( #create path sprite
               pos = (tile.x * tile_size, tile.y * tile_size), 
               surf = surf,
               groups = self.all_sprites,
               level = key)
          
    def input(self): # handles player input for dialogue and movement
      keys = pygame.key.get_pressed() #get all currently pressed keys

      if keys[pygame.K_SPACE]: #if space bar is pressed
            if not self.space_pressed:  #only trigger if space hasn't been processed yet
                self.space_pressed = True  #set flag that space is pressed

                if self.dialog_active: #if a dialogue is currently active
                    if self.dialog_manager.has_more_line(): #if there are more lines of dialogue
                      self.dialog_manager.next_line() #move to the next line of dialogue
                    else: #if the dialogue has ended
                     self.dialog_active = False #deactivate the dialogue mode
                     self.dialogue_finished = True #mark that the dialogue has finished
                     self.nearby_character = None #clear the reference to the current npc character
                elif self.nearby_character and not self.dialog_active: #if near a character and not currently in dialogue
                  self.dialog_manager.set_dialogue(self.nearby_character.dialog_text) #load that npc character's dialogue
                  self.dialog_active = True #activate dialogue mode
                  self.dialogue_finished = False #dialogue not yet finished
      else:
            self.space_pressed = False  #reset the flag when spacebar is released

      #handle Enter key for triggering character actions after dialogue ends
      if keys[pygame.K_RETURN] and self.dialog_active and not self.dialog_manager.has_more_line():
        if not hasattr(self,"enter_pressed"): # ensure the attribute exists
          self.enter_pressed = False #initialize enter_pressed

        if not self.enter_pressed and self.dialog_active and not self.dialog_manager.has_more_line():
          self.enter_pressed = True #flag that Enter as pressed so it's only triggered once
          print("Dialogue has finished")
          if self.nearby_character and self.nearby_character.action: #if a npc character has an action assigned
            self.nearby_character.action() #call the associated function that has been done earlier (eg., open store or battle)

          self.dialogue_finished = False #reset dialogue_finished flag
          self.nearby_character = None #clear reference to character

      else :
        self.enter_pressed = False #reset enter press if key is not held

      #movement control (only allow movement if no dialogue is active and icon is not currently moving)
      if self.current_node and not self.icon.path and not self.dialog_active:
        if keys[pygame.K_DOWN] and self.current_node.can_move("down"): #if down is pressed and movement is allowed
          self.move("down")
        if keys[pygame.K_LEFT] and self.current_node.can_move("left"): 
          self.move("left")
        if keys[pygame.K_RIGHT] and self.current_node.can_move("right"):
          self.move("right")
        if keys[pygame.K_UP] and self.current_node.can_move("up"):
          self.move("up")

    def move(self,direction): #move the icon along the specified direction's path
      path_key = int(self.current_node.paths[direction][0]) # get the path if from the node
      path_reverse = True if self.current_node.paths[direction][-1] == "r" else False #check if path should be reversed
      path = self.paths[path_key]["pos"][:] if not path_reverse else self.paths[path_key]["pos"][::-1] #get path positions, reversed if needed
      self.icon.start_move(path) #start moving the icon along the path

    def get_current_node(self): #update the current node the player is standing on
      nodes = pygame.sprite.spritecollide(self.icon, self.node_sprites, False) #check collision with any node
      if nodes:  #if there's at least one collision
        self.current_node = nodes[0] #set the current node to the one collided with

    def draw_dialog(self): #draw the dialogue box and text to the screen
      if self.dialog_active and self.dialog_manager.get_current_line(): #if dialogue is active and there's text to show
        box_rect = pygame.Rect(50, window_height - 150, window_width - 100, 100) #define the dialogue box rectangle
        pygame.draw.rect(self.display_surface, (0, 0, 0), box_rect) #draw black background for the dialogue box
        pygame.draw.rect(self.display_surface, (255, 255, 255), box_rect, 3) #draw white border around box

        text_surf = self.font.render(self.dialog_manager.get_current_line(), True, (255, 255, 255)) #render current line as white text
        self.display_surface.blit(text_surf, (box_rect.x + 20, box_rect.y + 30)) #blit the text onto the screen inside the box

    def run(self,dt): #main update and draw loop for the Overworld screen
        self.input() #handle player input
        self.get_current_node() #update the node the player is currently on
        if not self.dialog_active: #only check for nearby characters if not in a dialogue
          self.check_dialogue() #detect if a character is nearby for dialogue
        self.all_sprites.update(dt) #update all sprite animations and logic
        self.all_sprites.draw(self.icon.rect.center) #draw all sprites relative to icon's center

        if self.dialog_active: #if dialogue is happening
          self.draw_dialog() #draw the dialogue box and current line