from qx_settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self,pos,frames,groups):
        super().__init__(groups)

        self.frames, self.frame_index = frames, 0 
        self.facing_direction = "down"

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
    def __init__(self,pos,frames,groups):
        super().__init__(pos,frames,groups)
        self.z = Z_layers["main"]