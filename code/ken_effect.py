
import pygame
import sys
import time

class WeaponEffects:
    num_of_usage = {}

    @staticmethod
    def apply(name, mario, boss):

        max_usage = {
            "Thunder Axe": 1,
            "Essence of Renewal": 3,
            "Luna Bow": 1,
            "Hydro Strike": 1, 
            "Aegis Shield": 3,
            "Hawk's Eye": 1
        
        }

        if name in max_usage:
            WeaponEffects.num_of_usage.setdefault(name, 0)
            if WeaponEffects.num_of_usage[name] >= max_usage[name]:
                print(f"{name} has reached its usage limit. You can't use it anymore!")
                return
            WeaponEffects.num_of_usage[name] += 1

        effects = {
            "Thunder Axe": WeaponEffects.thunder_axe,
            "Essence of Renewal": WeaponEffects.essence_of_renewal,
            "Luna Bow": WeaponEffects.luna_bow,
            "Hydro Strike": WeaponEffects.hydro_strike,
            "Aegis Shield": WeaponEffects.aegis_shield,
            "Hawk's Eye": WeaponEffects.hawk_eye,

        }

        
        if name in effects:
            effects[name](mario, boss)
        else:
            print(f"No effect function for: {name}")

    @staticmethod
    def thunder_axe(mario, boss):
        if mario.attack_power == 100:  # only apply if attack power is normal
            mario.attack_power = 2000 # Boost Mario's attack power
            mario.power_timer = pygame.time.get_ticks() + 5000  # 5 seconds
            mario.active_weapon = "Thunder Axe"
            mario.activate_message = "Thunder Axe activated! Mario's attack power boosted to 180 for 15 seconds."
            mario.activate_message_timer = pygame.time.get_ticks() + 2000

    @staticmethod
    def essence_of_renewal(mario, boss):
        restore_health = 50
        mario.health += restore_health
        if mario.health > 100:
            mario.health = 100  # 不超过最大生命
            mario.active_weapon = "Essence of Renewal"
            mario.activate_message = f"Essence of Renewal activated! Mario restored {restore_health} HP."
            mario.activate_message_timer = pygame.time.get_ticks() + 2000

    @staticmethod
    def luna_bow(mario, boss):
        if mario.attack_power == 100:
            mario.attack_power = 2000
            mario.power_timer = pygame.time.get_ticks() + 5000
            mario.active_weapon = "Luna Bow"
            mario.activate_message = "Luna Bow activated! Mario's attack power boosted to 180 for 15 seconds."
            mario.activate_message_timer = pygame.time.get_ticks() + 2000

    @staticmethod
    def hydro_strike(mario, boss):
        if mario.attack_power == 100:
            mario.attack_power = 2000
            mario.power_timer = pygame.time.get_ticks() + 5000
            mario.active_weapon = "Hydro Strike"
            mario.activate_message = "Hydro Strike activated! Mario's attack power boosted to 180 for 15 seconds."
            mario.activate_message_timer = pygame.time.get_ticks() + 2000

    
    @staticmethod
    def aegis_shield(mario, boss):
        mario.shield = True
        mario.shield_timer = pygame.time.get_ticks() + 5000
        mario.active_weapon = "Aegis Shield"
        mario.activate_message = "Aegis Shield activated! Mario's attack power boosted to 180 for 15 seconds."
        mario.activate_message_timer = pygame.time.get_ticks() + 2000

    
    @staticmethod
    def hawk_eye(mario, boss):
        if mario.attack_power == 100:
            mario.attack_power = 2000
            mario.power_timer = pygame.time.get_ticks() + 5000
            mario.active_weapon = "Hawk's Eye"
            mario.activate_message = "Hawk's Eye activated! Mario's attack power boosted to 180 for 15 seconds."
            mario.activate_message_timer = pygame.time.get_ticks() + 2000


