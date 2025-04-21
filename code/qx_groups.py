from qx_settings import *

class WorldSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def draw(self,target_pos):
        self.offset.x = -(target_pos[0] - window_width / 2)
        self.offset.y = -(target_pos[1] - window_height / 2)

        for sprite in sorted(self,key = lambda sprite: sprite.z):
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)