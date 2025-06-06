import pygame
from qx_farm_settings import *
from qx_farm_player import Player
from qx_farm_tile import Tile
from qx_support import *
from random import choice, randint
from qx_farm_weapons import Weapon
from qx_farm_ui import UI
from qx_farm_enemy import Enemy
from qx_farm_particles import AnimationPlayer
from qx_farm_magic import MagicPlayer

class Level:
    def __init__(self,player_coins,player_diamonds,available_weapons,available_magic,username):

        self.game_over = False
        self.username = username

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #coins
        self.player_coins = player_coins
        self.player_diamonds = player_diamonds
        self.available_weapons = available_weapons
        self.weapons_index = 0
        self.weapon = self.available_weapons[self.weapons_index] if self.available_weapons else None
        self.available_magic = available_magic
        self.magic_index = 0
        self.magic = self.available_magic[self.magic_index] if self.available_magic else None

        #sprite
        self.create_map()

        #ui
        self.ui = UI(available_weapons,available_magic)

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layout = {
            "boundary" : import_csv_layout("farm_map/farming_map_FloorBlocks.csv"),
            "grass" : import_csv_layout("farm_map/farming_map_Grass.csv"),
            "object" : import_csv_layout("farm_map/farming_map_Objects.csv"),
            "entities" : import_csv_layout("farm_map/farming_map_Entities.csv")
        }
        
        graphics = {
            "grass" : import_folder_farm("graphics_qx/grass"),
            "objects" : import_folder_farm("graphics_qx/objects")
        }

        for style,layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x,y),[self.obstacles_sprites],"invisible")
                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites,self.attackable_sprites],"grass",random_grass_image)
                        
                        if style == "object":
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"object",surf)

                        if style == "entities":
                            if col == "394":
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacles_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                    coins=self.player_coins,
                                    diamonds=self.player_diamonds,
                                    available_weapons=self.available_weapons,
                                    available_magic=self.available_magic,
                                    username = self.username)
                            else:
                                if col == "390": monster_name = "bamboo"
                                elif col == "391": monster_name = "spirit"
                                elif col == "392": monster_name = "raccoon"
                                else: monster_name = "squid"
                                Enemy(monster_name,
                                      (x,y),
                                      [self.visible_sprites,self.attackable_sprites],
                                      self.obstacles_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles)

    def create_attack(self):
        if self.player.weapon:
            self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
        if style == "Essence of Renewal":
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

        if self.player.health <= 0:
            return True  # Signal that player died
        return False

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def run(self):
        #update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group): #craetes a camera that follows the player and has overlapping effect
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load("graphics_qx/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,"sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)