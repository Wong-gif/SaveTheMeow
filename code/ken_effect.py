import pygame
import random

YELLOW = (255, 255, 0)
LIGHT_GREEN = (144, 238, 144)
LIGHT_BLUE = (135, 206, 250)
LIGHT_PURPLE = (216, 191, 216)

class WeaponEffects:
    num_of_usage = {}

    @staticmethod
    def apply(name, mario, boss):

        max_usage = {
            "Phoenix Feather": 1,
            "Essence of Renewal": 3,
            "Luna Bow": 1,
            "Hydro Strike": 1, 
            "Aegis Shield": 3,
            "Hawk's Eye": 1
        }

        effects = {
            "Phoenix Feather": WeaponEffects.phoenix_feather,
            "Essence of Renewal": WeaponEffects.essence_of_renewal,
            "Luna Bow": WeaponEffects.luna_bow,
            "Hydro Strike": WeaponEffects.hydro_strike,
            "Aegis Shield": WeaponEffects.aegis_shield,
            "Hawk's Eye": WeaponEffects.hawk_eye,

        }


        if name in max_usage:
            WeaponEffects.num_of_usage.setdefault(name, 0)
            if WeaponEffects.num_of_usage[name] >= max_usage[name]:
                mario.activate_message = f"{name} has reached its usage limit. You can't use it anymore!"
                mario.activate_message_timer = pygame.time.get_ticks() + 2000
                return
            WeaponEffects.num_of_usage[name] += 1

        if name in effects:
            effects[name](mario, boss)
        else:
            mario.activate_message = f"No effect function for: {name}"
            mario.activate_message_timer = pygame.time.get_ticks() + 2000

    @staticmethod
    def phoenix_feather(mario, boss):
        if 80 <= mario.attack_power <= 100:  # only apply if attack power is normal
            mario.attack_power = random.randint(170, 190)  # Boost Mario's attack power
            mario.bullet_color = YELLOW
            mario.power_timer = pygame.time.get_ticks() + 5000  # 5 seconds
            mario.active_weapon = "Phoenix Feather"
            mario.activate_message = "Phoenix Feather activated! Mario's attack power boosted to 180 for 15 seconds."
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
        if 80 <= mario.attack_power <= 100:
            mario.attack_power = random.randint(150, 180)
            mario.bullet_color = LIGHT_GREEN   
            mario.power_timer = pygame.time.get_ticks() + 5000
            mario.active_weapon = "Luna Bow"
            mario.activate_message = "Luna Bow activated! Mario's attack power boosted to 180 for 15 seconds."
            mario.activate_message_timer = pygame.time.get_ticks() + 2000

    @staticmethod
    def hydro_strike(mario, boss):
        if 80 <= mario.attack_power <= 100:
            mario.attack_power = random.randint(210, 240)
            mario.bullet_color = LIGHT_BLUE
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
        if 80 <= mario.attack_power <= 100:
            mario.attack_power = random.randint(210, 225)
            mario.bullet_color = LIGHT_PURPLE
            mario.power_timer = pygame.time.get_ticks() + 5000
            mario.active_weapon = "Hawk's Eye"
            mario.activate_message = "Hawk's Eye activated! Mario's attack power boosted to 180 for 15 seconds."
            mario.activate_message_timer = pygame.time.get_ticks() + 2000


