
import pygame
import sys
import time

class WeaponEffects:
    active_effects = {} # Tracks how many left

    @staticmethod
    def apply(name, mario, boss):
        effects = {
            "Thunder Axe": WeaponEffects.thunder_axe,
        }
        if name in effects:
            effects[name](mario, boss)
        else:
            print(f"No effect function for: {name}")

    @staticmethod
    def thunder_axe(mario, boss):
        if mario.attack_power == 100:  # only apply if attack power is normal
            mario.attack_power = 2000 # Boost Mario's attack power
            mario.power_timer = pygame.time.get_ticks() + 5000  # 15 seconds
            print("Thunder Axe activated! Mario's attack power boosted to 180 for 15 seconds.")