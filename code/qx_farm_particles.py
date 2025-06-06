import pygame
from qx_support import import_folder_farm
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            #magic
            "flame" : import_folder_farm("graphics_qx/special_effects_farming/flame/frames"),
            "aura" : import_folder_farm("graphics_qx/special_effects_farming/aura"),
            "heal" : import_folder_farm("graphics_qx/special_effects_farming/heal/frames"),

            #attacks
            "claw" : import_folder_farm("graphics_qx/special_effects_farming/claw"),
            "slash" : import_folder_farm("graphics_qx/special_effects_farming/slash"),
            "sparkle" : import_folder_farm("graphics_qx/special_effects_farming/sparkle"),
            "leaf_attack" : import_folder_farm("graphics_qx/special_effects_farming/leaf_attack"),
            "thunder" : import_folder_farm("graphics_qx/special_effects_farming/thunder"),

            #monster deaths
            "squid" : import_folder_farm("graphics_qx/special_effects_farming/smoke_orange"),
            "raccoon" : import_folder_farm("graphics_qx/special_effects_farming/raccoon"),
            "spirit" : import_folder_farm("graphics_qx/special_effects_farming/nova"),
            "bamboo" : import_folder_farm("graphics_qx/special_effects_farming/bamboo"),

            #leafs
            "leaf" : (
                import_folder_farm("graphics_qx/special_effects_farming/leaf1"),
                import_folder_farm("graphics_qx/special_effects_farming/leaf2"),
                import_folder_farm("graphics_qx/special_effects_farming/leaf3"),
                import_folder_farm("graphics_qx/special_effects_farming/leaf4"),
                import_folder_farm("graphics_qx/special_effects_farming/leaf5"),
                import_folder_farm("graphics_qx/special_effects_farming/leaf6"),
                self.reflect_images(import_folder_farm("graphics_qx/special_effects_farming/leaf1")),
                self.reflect_images(import_folder_farm("graphics_qx/special_effects_farming/leaf2")),
                self.reflect_images(import_folder_farm("graphics_qx/special_effects_farming/leaf3")),
                self.reflect_images(import_folder_farm("graphics_qx/special_effects_farming/leaf4")),
                self.reflect_images(import_folder_farm("graphics_qx/special_effects_farming/leaf5")),
                self.reflect_images(import_folder_farm("graphics_qx/special_effects_farming/leaf6"))
            )
        }

    def reflect_images(self,frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames
    
    def create_grass_particles(self,pos,groups):
        animation_frames = choice(self.frames["leaf"])
        ParticlesEffect(pos,animation_frames,groups)

    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticlesEffect(pos,animation_frames,groups)



class ParticlesEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()