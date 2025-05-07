from qx_settings import *
from collections import deque #import deque for efficient queue-like behavior in dialogues

class Entity(pygame.sprite.Sprite): #base entity class for all animated characters (including players and npc)
    def __init__(self,pos,frames,groups,facing_direction):
        super().__init__(groups) #initialize as a Pygame sprite and add to groups

        self.frames, self.frame_index = frames, 0 # dictionary of animations based on its direction, starting frame index for animation
        self.facing_direction = facing_direction #direction the entity is facing (string)

        self.direction = vector() #vetor representing movement direction (initially zero)
        self.speed = 250 #movement speed in pixels per second

        #set the current image to the appropriate frame of the current animation
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(center = pos) # create rectangle for position and collision

    def animate(self,dt):   #a nimate the sprite based on delta time
        self.frame_index += animation_speed * dt #animation frame over time
        self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))] #get the correct animation list and loop through frames

    def get_state(self):     # deetermine current animation state
        moving = bool(self.direction) #check if there's any movement
        if moving: #if moving, update facing direction based on movement
            if self.direction.x != 0:
                self.facing_direction = "right" if self.facing_direction.x > 0 else "left"
            if self.facing_direction.y != 0:
                self.facing_direction = "down" if self.facing_direction.y > 0 else "up"
        #return current state string, append '_idle' if not moving
        return f"{self.facing_direction}{"" if moving else "_idle"}"
    
    #called every frame to update the entity
    def update(self,dt):
        self.animate(dt) #animate the character based on time passed

class Character(Entity): #class for npc
    def __init__(self,pos,frames,groups,facing_direction,action = None):
        super().__init__(pos,frames,groups,facing_direction)
        self.z = Z_layers["main"] #set drawing layer (z-index) from settings
        self.dialog_manager = DialogManager() #attach a DialogManager to handle dialogue
        self.action = action #function to trigger after dialogue

class DialogManager: #manages multi-line dialogues for characters
    def __init__(self):
        self.dialog_lines = deque() #queue of dialogue lines to display
        self.current_line = None #current line being shown

    def set_dialogue(self, dialogue_text): #set a new dialogue sequence into a list of strings
        self.dialog_lines = deque(dialogue_text) #convert list to deque
        self.current_line = self.dialog_lines.popleft() if self.dialog_lines else None #pop and set the first line, or None if the list was empty

    def next_line(self): #proceed to the next line of dialogue
        if self.dialog_lines: #if there are more lines
            self.current_line = self.dialog_lines.popleft() #show the next one
        else:
            self.current_line = None #no more lines to show

    def get_current_line(self): #get the current line of dialogue
        return self.current_line

    def has_more_line(self): #check if there are more lines left in the dialogue
        return bool(self.dialog_lines) #return True if deque is not empty