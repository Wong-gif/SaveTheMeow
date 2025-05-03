from qx_settings import *
from collections import deque

class Entity(pygame.sprite.Sprite):
    def __init__(self,pos,frames,groups,facing_direction):
        super().__init__(groups)

        self.frames, self.frame_index = frames, 0 
        self.facing_direction = facing_direction

        self.direction = vector()
        self.speed = 250

        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def animate(self,dt):  
        self.frame_index += animation_speed * dt
        self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x != 0:
                self.facing_direction = "right" if self.facing_direction.x > 0 else "left"
            if self.facing_direction.y != 0:
                self.facing_direction = "down" if self.facing_direction.y > 0 else "up"
        return f"{self.facing_direction}{"" if moving else "_idle"}"

    def update(self,dt):
        self.animate(dt)

class Character(Entity):
    def __init__(self,pos,frames,groups,facing_direction):
        super().__init__(pos,frames,groups,facing_direction)
        self.z = Z_layers["main"]
        self.dialog_manager = DialogManager()

class DialogManager:
    def __init__(self):
        self.dialog_lines = deque
        self.current_line = None

    def set_dialogue(self,dialogue_text):
        self.dialogue_lines = deque(dialogue_text)
        self.current_line = self.dialogue_lines.popleft() if self.dialogue_lines else None

    def next_line(self):
        if self.dialogue_lines:
            self.current_line = self.dialogue_lines.popleft()
        else:
            self.current_line = None

    def get_current_line(self):
        return self.current_line
    
    def has_more_line(self):
        return bool(self.dialog_lines)