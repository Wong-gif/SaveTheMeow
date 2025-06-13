import pygame
from qx_farm_settings import *
from qx_support import *
from qx_farm_entity import Entity
import json

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic,coins=0,diamonds=0,available_magic=None, available_weapons=None, username=None):
        super().__init__(groups)
        self.image = pygame.image.load("graphics_qx/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-25,HITBOX_OFFSET["player"])

        self.username = username

        #graphics
        self.import_player_assets()
        self.status = "down"

        #movement
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = None
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        #weapons
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.available_weapons = available_weapons if available_weapons else []
        self.weapons_index = 0
        self.weapon = self.available_weapons[self.weapons_index] if self.available_weapons else None

        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        #magic
        self.create_magic = create_magic
        self.available_magic = available_magic if available_magic else []
        self.magic_index = 0
        self.magic = self.available_magic[self.magic_index] if self.available_magic else None
        self.can_switch_magic = True
        self.magic_switch_time = None

        #stats
        self.stats = {"health":100, "attack":10, "magic":4, "speed":5}
        self.health = self.stats["health"]
        self.coins = coins
        self.diamonds = diamonds

        self.speed = self.stats["speed"]

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.game3_coins = 0
        self.game3_diamonds = 0
        self.load_game3_data()

    def load_game3_data(self):
        """Load ONLY game3 coins and diamonds (separate from main currency)"""
        try:
            with open(f"{self.username}.txt", "r") as f:
                data = json.load(f)
            if "game3" in data:
                self.game3_coins = data["game3"].get("Coins", 0)
                self.game3_diamonds = data["game3"].get("Diamonds", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def add_coins(self, amount):
        """Add coins to Game 3 only (doesn't affect main coins)"""
        self.game3_coins += amount
        print(f"Added {amount} coins. Total: {self.game3_coins}")  # Debug print
        self.save_game3_data()  # Save immediately
        
    def add_diamonds(self, amount):
        """Add diamonds to Game 3 only (doesn't affect main diamonds)"""
        self.game3_diamonds += amount
        print(f"Added {amount} diamonds. Total: {self.game3_diamonds}")  # Debug print
        self.save_game3_data()  # Save immediately
        
    def save_game3_data(self):
        """Save current Game 3 coins and diamonds (separate from main currency)"""
        try:
            with open(f"{self.username}.txt", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
            
        if "game3" not in data:
            data["game3"] = {"Coins": 0, "Diamonds": 0}
            
        data["game3"]["Coins"] = self.game3_coins
        data["game3"]["Diamonds"] = self.game3_diamonds
        
        with open(f"{self.username}.txt", "w") as f:
            json.dump(data, f)
        print("Game3 data saved!")  # Debug print

    def import_player_assets(self):
        character_path = "graphics_qx/player/"
        self.animations = {"up":[], "down":[],"left":[],"right":[],
                           "right_idle":[], "left_idle":[],"up_idle":[],"down_idle":[],
                           "right_attack":[],"left_attack":[],"up_attack":[],"down_attack":[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder_farm(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            
            #movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:   
                self.direction.x = 0

            #attack input
            if keys[pygame.K_SPACE] and self.weapon is not None:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.attack_cooldown = weapons_data[self.weapon]["cooldown"]
                self.create_attack()

            #special powers input
            if keys[pygame.K_LCTRL] and self.magic is not None:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                magic_info = magic_data[self.magic]
                style = self.magic
                strength = magic_info["strength"] + self.stats["magic"]
                self.create_magic(style, strength)

            if keys[pygame.K_q] and self.can_switch_weapon:
                if len(self.available_weapons) > 1:
                    self.can_switch_weapon = False
                    self.weapon_switch_time = pygame.time.get_ticks()

                    self.weapons_index = (self.weapons_index + 1) % len(self.available_weapons)
                    self.weapon = self.available_weapons[self.weapons_index]
                    if self.attacking:
                        self.destroy_attack()
                        self.attacking = False

            if keys[pygame.K_e] and self.can_switch_magic:
                if len(self.available_magic) > 1:
                    self.can_switch_magic = False
                    self.magic_switch_time = pygame.time.get_ticks()
                    self.magic_index = (self.magic_index + 1) % len(self.available_magic)
                    self.magic = self.available_magic[self.magic_index]

    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    #overwrite idle
                    self.status = self.status.replace("_idle","_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack","")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        #looping the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        if self.weapon is None:
            return self.stats["attack"]
        base_damage = self.stats["attack"]
        weapon_damage = weapons_data[self.weapon]["damage"]
        return base_damage + weapon_damage
    
    def check_death(self):
        if self.health <= 0:
            return True
        return False

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.check_death()