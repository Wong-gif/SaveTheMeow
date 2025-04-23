from qx_settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf = pygame.Surface((tile_size,tile_size)),groups = None, z = Z_layers["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite):
    def __init__ (self, pos, frames, groups, z = Z_layers["main"], animation_speed = animation_speed):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos,self.frames[self.frame_index],groups,z)
        self.animation_speed = animation_speed

    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self,dt):
        self.animate(dt)

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,level,data):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (pos[0] + tile_size/2, pos[1] + tile_size/2))
        self.z = Z_layers["path"]
        self.level = level
        self.data = data

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos,groups,frames):
        super().__init__(groups)
        self.icon = True

        #images
        self.frames, self.frame_index = frames, 0
        self.state = "idle"
        self.image = self.frames[self.state][self.frame_index]
        self.z = Z_layers["main"]

        #rect
        self.rect = self.image.get_frect(center = pos)