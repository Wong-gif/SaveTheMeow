import pygame
import sys

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800 

class GameSummary:
    def __init__(self, screen, levels_data, game1_coins, game2_coins, game1_diamonds, game2_diamonds):
        self.screen = screen
        self.levels_data = levels_data
        self.game1_coins = game1_coins
        self.game2_coins = game2_coins
        self.game1_diamonds = game1_diamonds
        self.game2_diamonds = game2_diamonds
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)

        self.arrow_img = pygame.image.load("assets/images/arrow1/arrow.png").convert_alpha()
        self.arrow_rect = self.arrow_img.get_rect(topleft=(20, 20))  

        self.background = pygame.image.load('assets/images/good.png').convert()
        self.background = pygame.transform.scale(self.background, (1200, 800))


    def run(self):
        running = True
        while running:
            self.screen.fill((10, 10, 30))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.arrow_img, self.arrow_rect.topleft)

            for level_name, data in self.levels_data.items():
                if level_name == "level1":
                    level_text = self.font.render("Game 1", True, (255, 255, 0))
                    coin_text = self.small_font.render(f"Coins: {data['coins']}", True, (0, 0, 0))
                    diamond_text = self.small_font.render(f"Diamonds: {data['diamonds']}", True, (0, 0, 0))
                    self.screen.blit(level_text, (800, 400))
                    self.screen.blit(coin_text, (800, 490))
                    self.screen.blit(diamond_text, (800, 580))
                elif level_name == "level2":
                    level_text = self.font.render("Game 2", True, (255, 255, 0))
                    coin_text = self.small_font.render(f"Coins: {data['coins']}", True, (255, 255, 255))
                    diamond_text = self.small_font.render(f"Diamonds: {data['diamonds']}", True, (255, 255, 255))
                    self.screen.blit(level_text, (240, 50))
                    self.screen.blit(coin_text, (240, 140))
                    self.screen.blit(diamond_text, (240, 230))


            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "menu"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.arrow_rect.collidepoint(event.pos):
                        return "menu"
                    





import pygame
import random
import json
import os
from jh_death_popup import DeathPopup


def save_game2_data(username, coin, diamond):
    try:
        filename = f"{username}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                user_data = json.load(file)
        else:
            user_data = {
                "game1": {},
                "game2": {}
            }

        user_data["game2"]["Coins"] = coin
        user_data["game2"]["Diamonds"] = diamond

        best_coin = user_data["game2"].get("Best Coins", 0)
        best_diamond = user_data["game2"].get("Best Diamonds", 0)

        user_data["game2"]["Best Coins"] = max(coin, best_coin)
        user_data["game2"]["Best Diamonds"] = max(diamond, best_diamond)

        with open(filename, "w") as file:
            json.dump(user_data, file, indent=4)

        print("Game 2 data saved successfully!")
    except Exception as e:
        print("Failed to save Game 2 data:", e)

class Button:
    def __init__(self, normal_image, pressed_image, x, y):
        self.normal_image = normal_image
        self.pressed_image = pressed_image
        self.image = normal_image
        self.world_x = x
        self.world_y = y
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.world_x - camera_x, self.world_y))

    def check_player_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.image = self.pressed_image
            return True
        return False
    
class Spring(pygame.sprite.Sprite):
    def __init__(self, normal_image, pressed_image, x, y):
        super().__init__()
        self.normal_image = normal_image
        self.pressed_image = pressed_image
        self.image = normal_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pressed = False
        self.press_timer = 0

    def press(self):
        self.pressed = True
        self.image = self.pressed_image
        self.press_timer = 0

    def update(self):
        if self.pressed:
            self.press_timer += 1
            if self.press_timer > 10:
                self.pressed = False
                self.image = self.normal_image
                self.press_timer = 0
   
class Game2:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = screen.get_size()
        self.world_width = 3200 
        self.camera_x = 0
        self.state = "playing"
        self.score = 0
        self.time_left = 40        
    
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 27)

        self.coins_collected = 0
        self.diamonds_collected = 0

        self._load_game_assets()

        self.player_rect = self.player_images['idle'].get_rect()
        self.player_rect.midbottom = (160, 70)  # player position
        self.player_speed = 5
        self.velocity_y = 0
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        self.animation_speed = 0.15

        self.death_popup = DeathPopup(screen, self.screen_width, self.screen_height)
        
        self.portal_rect = pygame.Rect(3100, 221, 80, 100)  # 位置自己调  
        self.portal_frames = []
        for i in range(16):
            frame = pygame.image.load(f"assets/images/portal/portal_{i}.png").convert_alpha()
            self.portal_frames.append(frame)   

        self.portal_frame_index = 0
        self.portal_frame_timer = 0
        self.level_start_time = pygame.time.get_ticks()     

        self.fireballs = []  # 火球列表
        self.fireball_image = pygame.image.load("assets/images/fireball.png").convert_alpha()

        for i in range(5):
            x = 3200
            y = random.randint(250, 600)
            speed = random.randint(3, 6)
            self.fireballs.append({"rect": pygame.Rect(x, y, 40, 40), "speed": speed})

    def _load_game_assets(self):
        self.jump_sound = pygame.mixer.Sound('assets/sounds/player_jump.wav')
        self.jump_sound.set_volume(0.2)
        self.diamond_sound = pygame.mixer.Sound("assets/sounds/diamond.wav")
        self.diamond_sound.set_volume(4.0)
        self.coin_sound = pygame.mixer.Sound('assets/sounds/coin.wav')
        self.coin_sound.set_volume(0.3)

        self.coin_icon = pygame.image.load("assets/images/ui/coin_icon.png").convert_alpha()
        self.time_icon = pygame.image.load("assets/images/ui/time_icon.png").convert_alpha()
        self.diamond_icon = pygame.image.load("assets/images/ui/diamond_icon.png").convert_alpha()

        self.dian_image = pygame.image.load("assets/images/dian.png").convert_alpha()

        self.last_time_update = pygame.time.get_ticks()# time setting in order to reduce timing
        self.spike_image = pygame.image.load("assets/images/spike.png").convert_alpha()

        self.spike_visible = False # make the spike cannot see first
        self.spike_rect = self.spike_image.get_rect()
        self.spike_rect.topleft = (930, 555) # 1st spike position 

        self.spike1_rect = self.spike_image.get_rect()
        self.spike1_rect.topleft = (2000, 555)
        self.spike2_rect = self.spike_image.get_rect()
        self.spike2_rect.topleft = (2030, 555)
        self.spike3_rect = self.spike_image.get_rect()
        self.spike3_rect.topleft = (2060, 555)

        self.spike4_rect = self.spike_image.get_rect()
        self.spike4_rect.topleft = (2220, 555)
        self.spike5_rect = self.spike_image.get_rect()
        self.spike5_rect.topleft = (2250, 555)
        self.spike6_rect = self.spike_image.get_rect()
        self.spike6_rect.topleft = (2280, 555)

        self.spike7_rect = self.spike_image.get_rect()
        self.spike7_rect.topleft = (2440, 555)
        self.spike8_rect = self.spike_image.get_rect()
        self.spike8_rect.topleft = (2470, 555)
        self.spike9_rect = self.spike_image.get_rect()
        self.spike9_rect.topleft = (2500, 555)

        self.spring_normal = pygame.image.load("assets/images/spring_normal.png").convert_alpha()
        self.spring_pressed = pygame.image.load("assets/images/spring_pressed.png").convert_alpha()
        self.spring = Spring(self.spring_normal, self.spring_pressed, 2600, self.screen_height - 350)
               
        self.button_normal = pygame.image.load("assets/images/button_normal.png").convert_alpha()
        self.button_pressed = pygame.image.load("assets/images/button_pressed.png").convert_alpha()
        self.button = Button(self.button_normal, self.button_pressed, 0, self.screen_height - 250)
        self.button2 = Button(self.button_normal, self.button_pressed, 700, self.screen_height - 250)

        self.platform_image = pygame.image.load("assets/images/rui.png").convert_alpha()
        self.platform_rect = self.platform_image.get_rect()
        self.platform_rect.midbottom = (490, 500)  # platform position
        self.platform_visible = False  # same as the top, cannot see first

        self.platform2_image = pygame.image.load("assets/images/rui.png").convert_alpha()
        self.platform2_rect = self.platform2_image.get_rect()
        self.platform2_rect.midbottom = (1300, 580) 
        self.platform2_visible = False

        self.platform3_image = pygame.image.load("assets/images/rui.png").convert_alpha()
        self.platform3_rect = self.platform3_image.get_rect()
        self.platform3_rect.midbottom = (1550, 510)  
        self.platform3_visible = False 

        self.platform4_image = pygame.image.load("assets/images/rui.png").convert_alpha()
        self.platform4_rect = self.platform4_image.get_rect()
        self.platform4_rect.midbottom = (1800, 440) 
        self.platform4_visible = False

        sky = pygame.image.load("assets/images/level2_background.png").convert()
        sky = pygame.transform.smoothscale(sky, (3200, self.screen_height))
        self.background = sky

        self.ground_image_full = pygame.image.load("assets/images/platform.png").convert_alpha()
        self.ground_image_full = pygame.transform.smoothscale(self.ground_image_full, (self.world_width, 100))

        diamond_positions = [
        (700, 300),
        (600, 350),
        (860, 480),
        (1100, 400),
        (2300, 480),
        (2200, 500),
    ]

        self.diamond = []
        for pos in diamond_positions:
            x, y = pos
            diamond_rect = pygame.Rect(x, y, 30, 30)
            self.diamond.append({
                "rect": diamond_rect,
            })

        self.coin_frames = [
            self._load_single_image("assets/images/coin/coin_frame_1.png"),
            self._load_single_image("assets/images/coin/coin_frame_2.png"),
            self._load_single_image("assets/images/coin/coin_frame_3.png"),
            self._load_single_image("assets/images/coin/coin_frame_4.png"),
            self._load_single_image("assets/images/coin/coin_frame_5.png"),
            self._load_single_image("assets/images/coin/coin_frame_6.png"),
        ]

        coin_positions = [
        (500, 200),
        (700, 450),
        (1000, 450),
        (1500, 430),
        (2000, 480),
        (2500, 500),
        (2700, 200),
        (2730, 200),
    ]
        
        self.coins = []
        for pos in coin_positions:
            x, y = pos
            coin_rect = pygame.Rect(x, y, 30, 30)
            self.coins.append({
                "rect": coin_rect,
                "frame": 0,
                "animation_speed": 0.2
            })


        self.player_images = {
            'idle': self._load_single_image("assets/images/player/player_stand.png"),
            'walk': [
                self._load_single_image("assets/images/player/player_walk1.png"),
                self._load_single_image("assets/images/player/player_walk2.png")
            ],
            'jump': self._load_single_image("assets/images/player/player_stand.png")
        }

import pygame
import random
import os
import json
from jh_death_popup import DeathPopup


def save_game1_data(username, coin, diamond):
    try:
        filename = f"{username}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                user_data = json.load(file)
        else:
            user_data = {
                "game1": {},
                "game2": {}
            }
            
        user_data["game1"]["Coins"] = coin
        user_data["game1"]["Diamonds"] = diamond

        best_coin = user_data["game1"].get("Best Coins", 0)
        best_diamond = user_data["game1"].get("Best Diamonds", 0)

        user_data["game1"]["Best Coins"] = max(coin, best_coin)
        user_data["game1"]["Best Diamonds"] = max(diamond, best_diamond)

        with open(filename, "w") as file:
            json.dump(user_data, file, indent=4)

        print("Game 1 data saved successfully!")
    except Exception as e:
        print("Failed to save Game 1 data:", e)
