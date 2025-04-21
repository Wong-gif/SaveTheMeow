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