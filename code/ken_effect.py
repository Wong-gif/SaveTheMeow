import pygame
import random
import json

class WeaponEffects:

        max_usage = {
            "Phoenix Feather": 1,
            "Essence of Renewal": 3,
            "Luna Bow": 1,
            "Hydro Strike": 1, 
            "Aegis Shield": 5,
            "Hawk's Eye": 1
        }
        
        duration = {
            "Phoenix Feather": 7000,
            "Luna Bow": 12000,
            "Hydro Strike": 7000,
            "Aegis Shield": 8000,
            "Hawk's Eye": 10000
        }

        # 类变量
        num_of_usage = {}
        cooldowns = {}

        #@staticmethod
        #def load_usage(username):
            ##try:
                #with open(f"{username}_weapons.json", "r") as f:
                    #WeaponEffects.num_of_usage = json.load(f)
            #except:
                #WeaponEffects.num_of_usage = {}

        #@staticmethod
        #def save_usage(username):
            #"""保存使用次数到存档"""
            #with open(f"{username}_weapons.json", "w") as f:
                #json.dump(WeaponEffects.num_of_usage, f)

        @staticmethod
        def apply(name, mario, boss):
            # 检查冷却
            now = pygame.time.get_ticks()
            
            if name in WeaponEffects.max_usage:
                WeaponEffects.num_of_usage.setdefault(name, 0)
                if WeaponEffects.num_of_usage[name] >= WeaponEffects.max_usage[name]:
                    mario.activate_message = f"{name} has reached its usage limit. You can't use it anymore!"
                    mario.activate_message_timer = pygame.time.get_ticks() + 2000
                    return False
                WeaponEffects.num_of_usage[name] += 1

            effect_method = getattr(WeaponEffects, name.lower().replace(" ", "_"), None)
            if effect_method:
                effect_method(mario, boss)
                return True
            
            mario.activate_message = f"Invalid weapon: {name}"
            mario.activate_message_timer = now + 2000
            return False

        @staticmethod
        def phoenix_feather(mario, boss):
            if 80 <= mario.attack_power <= 100:  # only apply if attack power is normal
                mario.attack_power = random.randint(120, 140)  # Boost Mario's attack power
                mario.power_timer = pygame.time.get_ticks() + WeaponEffects.duration["Phoenix Feather"]
                mario.active_weapon = "Phoenix Feather"
                mario.activate_message = "Phoenix Feather activated! Mario's attack power boosted for 7 seconds."
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
                mario.attack_power = random.randint(120, 145)  
                mario.power_timer = pygame.time.get_ticks() +  WeaponEffects.duration["Luna Bow"]
                mario.active_weapon = "Luna Bow"
                mario.activate_message = "Luna Bow activated! Mario's attack power boosted for 12 seconds."
                mario.activate_message_timer = pygame.time.get_ticks() + 2000

        @staticmethod
        def hydro_strike(mario, boss):
            if 80 <= mario.attack_power <= 100:
                mario.attack_power = random.randint(200, 220)
                mario.power_timer = pygame.time.get_ticks() +  WeaponEffects.duration["Hydro Strike"]
                mario.active_weapon = "Hydro Strike"
                mario.activate_message = "Hydro Strike activated! Mario's attack power boosted for 7 seconds."
                mario.activate_message_timer = pygame.time.get_ticks() + 2000

        
        @staticmethod
        def aegis_shield(mario, boss):
            mario.shield = True
            mario.shield_timer = pygame.time.get_ticks() +  WeaponEffects.duration["Aegis Shield"]
            mario.active_weapon = "Aegis Shield"
            mario.activate_message = "Aegis Shield activated! Mario's defense is enhanced for 8 seconds."
            mario.activate_message_timer = pygame.time.get_ticks() + 2000

        
        @staticmethod
        def hawk_eye(mario, boss):
            if 80 <= mario.attack_power <= 100:
                mario.attack_power = random.randint(145, 165)
                mario.power_timer = pygame.time.get_ticks() +  WeaponEffects.duration["Hawk's Eye"]
                mario.active_weapon = "Hawk's Eye"
                mario.activate_message = "Hawk's Eye activated! Mario's attack power boosted for 10 seconds."
                mario.activate_message_timer = pygame.time.get_ticks() + 2000


