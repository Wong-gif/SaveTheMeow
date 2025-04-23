from qx_settings import *

class WorldSprites(pygame.sprite.Group):
    def __init__(self,data):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.offset = vector()

    def draw(self,target_pos):
        self.offset.x = -(target_pos[0] - window_width / 2)
        self.offset.y = -(target_pos[1] - window_height / 2)
        #background
        for sprite in sorted(self,key = lambda sprite: sprite.z):
            if sprite.z < Z_layers["main"]:
              if sprite.z == Z_layers["path"]:
                if sprite.level <= self.data.unlocked_level:
                 self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
              else:
                 self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        #main
        for sprite in sorted(self, key = lambda sprite: sprite.rect.centery):
            if sprite.z == Z_layers["main"]:
                if hasattr(sprite, "icon"):
                 self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset + vector(0,-28))  
                else:
                 self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)