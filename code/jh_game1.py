'''import pygame
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

class Game1:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.SysFont('Arial', 32)
        self.has_printed_success = False 
        self.world_width = 3200
        self.camera_x = 0
        self.state = "playing"
        self.score = 0
        self.time_left = 30
        self.last_time_update = pygame.time.get_ticks()
        self.portal_frame_index = 0 
        self.portal_animation_speed = 0.2
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 27)

        self.level_start_time = pygame.time.get_ticks()
        self.time_used = 0

        self.coins_collected = 0
        self.diamonds_collected = 0

        self.coin_icon = pygame.image.load("assets/images/ui/coin_icon.png").convert_alpha()
        self.time_icon = pygame.image.load("assets/images/ui/time_icon.png").convert_alpha()
        self.diamond_icon = pygame.image.load("assets/images/ui/diamond_icon.png").convert_alpha()
        self.dian_image = pygame.image.load("assets/images/dian.png").convert_alpha()

        self.jump_sound = pygame.mixer.Sound('assets/sounds/player_jump.wav')
        self.jump_sound.set_volume(0.2)
        self.dian_sound = pygame.mixer.Sound("assets/sounds/dian.wav") 
        self.dian_sound.set_volume(2.0)
        self.diamond_sound = pygame.mixer.Sound("assets/sounds/diamond.wav")
        self.diamond_sound.set_volume(4.0)
        self.coin_sound = pygame.mixer.Sound('assets/sounds/coin.wav')
        self.coin_sound.set_volume(0.3)

        self.death_popup = DeathPopup(screen, self.screen_width, self.screen_height)
        
        self._load_game_assets()

        self.player_rect = self.player_images['idle'].get_rect()
        self.player_rect.midbottom = (140, 70)
        self.player_speed = 5
        self.velocity_y = 0
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        self.animation_speed = 0.15

        self.split_positions = [1000, 2500]
        self.split_progresses = [0 for _ in self.split_positions]
        self.split_width = 220
        self.ground_split_flags = [False for _ in self.split_positions]

        self.coins = []
        for _ in range(12):         
            x = random.randint(100, self.world_width - 100)
            y = random.randint(300, 495)
            coin_rect = pygame.Rect(x, y, 30, 30)
            self.coins.append({
                "rect": coin_rect,
                "frame": 0,
                "animation_speed": 0.2
            })

        self.diamond = []
        for _ in range(5):  
            x = random.randint(100, self.world_width - 100)
            y = random.randint(300, 495)
            diamond_rect = pygame.Rect(x, y, 30, 30)
            self.diamond.append({
                "rect": diamond_rect
            })

        self.portal_frames = []
        for i in range(16):
            frame = pygame.image.load(f"assets/images/portal/portal_{i}.png").convert_alpha()
            self.portal_frames.append(frame)

        self.dians = [
            {"rect": pygame.Rect(450, 500, 40, 40), "collected": False},   
            {"rect": pygame.Rect(620, 500, 40, 40), "collected": False},  
            {"rect": pygame.Rect(790, 500, 40, 40), "collected": False},  
        ]

        self.bricks = [
            {"rect": pygame.Rect(350, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1600, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1850, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1890, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(2800, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(3100, 521, 40, 40), "type": "portal", "active": True}
        ]

    def _load_game_assets(self):

        sky = pygame.image.load("assets/images/level1_background.png").convert()
        sky = pygame.transform.smoothscale(sky, (self.screen_width, self.screen_height))

        self.background = pygame.Surface((self.world_width, self.screen_height))
        for x in range(0, self.world_width, self.screen_width):
            self.background.blit(sky, (x, 0))

        self.ground_image_full = pygame.image.load("assets/images/ground.png").convert_alpha()
        self.ground_image_full = pygame.transform.smoothscale(self.ground_image_full, (self.world_width, 100))

        self._placeholder = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self._placeholder, (255, 0, 255), (0, 0, 32, 32))
        
        self.player_images = {
            'idle': self._load_single_image("assets/images/player/player_stand.png"),
            'walk': [
                self._load_single_image("assets/images/player/player_walk1.png"),
                self._load_single_image("assets/images/player/player_walk2.png")
                ],
            'jump': self._load_single_image("assets/images/player/player_stand.png")
        }

        self.coin_frames = [
            self._load_single_image("assets/images/coin/coin_frame_1.png"),
            self._load_single_image("assets/images/coin/coin_frame_2.png"),
            self._load_single_image("assets/images/coin/coin_frame_3.png"),
            self._load_single_image("assets/images/coin/coin_frame_4.png"),
            self._load_single_image("assets/images/coin/coin_frame_5.png"),
            self._load_single_image("assets/images/coin/coin_frame_6.png"),
        ]

        self.spike_image = self._load_single_image("assets/images/spike.png")


    def _load_single_image(self, path):
        image = pygame.image.load(path).convert_alpha()  # 使用透明通道加载图片
        image.set_colorkey((0, 255, 255))  # 设置青色为透明（0, 255, 255）
        return image
    
    def update_camera(self):
        target_x = self.player_rect.centerx - self.screen_width // 2
        self.camera_x = max(0, min(target_x, self.world_width - self.screen_width))

    def world_to_screen(self, rect):
        return rect.move(-self.camera_x, 0)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= self.player_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed
            self.facing_right = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            self.jump_sound.play()

    # time setting
    def update_physics(self):
        current_time = pygame.time.get_ticks()
        
        if self.state == "playing" and current_time - self.last_time_update > 1000:
            self.time_left -= 1
            self.last_time_update = current_time
            if self.time_left <= 0:
                self.death_popup.show("Time's up! Game over!")
                return
        
        self.velocity_y += self.gravity
        self.player_rect.y += self.velocity_y
        self.portal_frame_index += self.portal_animation_speed
        if self.portal_frame_index >= len(self.portal_frames):
           self.portal_frame_index = 0

        for coin in self.coins:
            coin["frame"] += coin["animation_speed"]
            if coin["frame"] >= len(self.coin_frames):
                coin["frame"] = 0 

        for coin in self.coins[:]: 
            if self.player_rect.colliderect(coin["rect"]):
                self.coins.remove(coin)
                self.coins_collected += 20
                self.score += 20
                self.coin_sound.play()
                
        for diamond in self.diamond[:]: 
            if self.player_rect.colliderect(diamond["rect"]):
                self.diamond.remove(diamond)
                self.diamonds_collected += 10 
                self.score += 10
                self.diamond_sound.play()
                                   
        #ground material        
        for i, pos in enumerate(self.split_positions):
            if not self.ground_split_flags[i] and abs(self.player_rect.centerx - pos) < 200:
                self.ground_split_flags[i] = True
            if self.ground_split_flags[i] and self.split_progresses[i] < self.split_width:
                self.split_progresses[i] += 22 # the speed of open the ground

        self.on_ground = False
        for start_x, width in self.generate_ground_segments():
            ground_rect = pygame.Rect(start_x, 605, width, 100)
            if self.player_rect.colliderect(ground_rect):
                self.on_ground = True
                self.player_rect.bottom = ground_rect.top
                self.velocity_y = 0
                break

        for index, dian in enumerate(self.dians):
            if not dian["collected"] and self.player_rect.colliderect(dian["rect"]):
                if index == 1:
                    self.death_popup.show("Please be advised not to place trust in any ball!")
                    return
                else:
                    dian["collected"] = True
                    self.dian_sound.play()
               
        if self.player_rect.bottom > self.screen_height:
            self.death_popup.show("You fell off the ground!")
            return
        
        for brick in self.bricks:
            if brick["type"] == "spike" and brick["active"]:
                if not brick.get("visible", False):
                    if abs(self.player_rect.centerx - brick["rect"].centerx) < 80:
                        brick["visible"] = True
                        brick["rect"].y -= 30

        for brick in self.bricks:
            if brick["type"] == "spike" and brick["active"]:
                if self.player_rect.colliderect(brick["rect"]):
                    self.death_popup.show("Caution! You have been slain by deadly spikes!")
                    return
                    
        for brick in self.bricks:
            if brick["type"] == "portal" and brick["active"]:
                if self.player_rect.colliderect(brick["rect"]):
                    if self.state != "next_level":
                        self.time_used = pygame.time.get_ticks() - self.level_start_time
                        self.state = "next_level"

                        if not self.has_printed_success:
                           print("Congratulations!")

                           save_game1_data(
                               username=self.username,
                               coin=self.coins_collected,
                               diamond=self.diamonds_collected,
                               #time_taken=self.time_used / 1000
                           )

                           self.has_printed_success = True
                                        
        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(self.world_width, self.player_rect.right)

        self.update_camera()
        self.animation_frame += self.animation_speed

    def generate_ground_segments(self):
        ground_segments = []
        last_x = 0
        for i, pos in enumerate(self.split_positions):
            progress = self.split_progresses[i]
            gap_start = pos - progress // 2
            gap_end = pos + progress // 2

        # 左边的地面段
            if gap_start > last_x:
                ground_segments.append((last_x, gap_start - last_x))  # (起点x, 宽度)

            last_x = gap_end

    # 最后一段地面
        if last_x < self.world_width:
            ground_segments.append((last_x, self.world_width - last_x))

        return ground_segments
    
    def get_player_image(self):
        if not self.on_ground:# if not in ground， run jump photo
            return self.player_images['jump']
        moving = pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]
        if moving:
            frame_index = int(self.animation_frame) % len(self.player_images['walk'])
            return self.player_images['walk'][frame_index]
        return self.player_images['idle']#if not moving anyone, run idle photo

    def draw(self):
        self.screen.blit(self.background, (-self.camera_x, 0))
        # ground crack
        for start_x, width in self.generate_ground_segments():
            if width > 0:
                ground_surface = self.ground_image_full.subsurface((start_x, 0, width, 100))
                self.screen.blit(ground_surface, (start_x - self.camera_x, 600))

        for coin in self.coins:
            frame_index = int(coin["frame"]) % len(self.coin_frames)
            image = self.coin_frames[frame_index]
            self.screen.blit(image, self.world_to_screen(coin["rect"]))

        for diamond in self.diamond:
            self.screen.blit(self.diamond_icon, self.world_to_screen(diamond["rect"]))
           
        for brick in self.bricks:
            if not brick["active"]:
                continue
            if brick["type"] == "spike" and brick.get("visible", False):
                self.screen.blit(self.spike_image, self.world_to_screen(brick["rect"]))
            elif brick["type"] == "portal" and brick["active"]:
                frame_index = int(self.portal_frame_index) % len(self.portal_frames)
                frame = self.portal_frames[frame_index]
                self.screen.blit(frame, self.world_to_screen(brick["rect"]))

        for dian in self.dians:
            if not dian["collected"]:
                self.screen.blit(self.dian_image, self.world_to_screen(dian["rect"]))
                
        current_image = self.get_player_image()# talking about the player face, when the player turn right face follow right.
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        self.screen.blit(current_image, self.world_to_screen(self.player_rect))
       
        ui_bar = pygame.Surface((380, 50), pygame.SRCALPHA)
        self.screen.blit(ui_bar, (20, 20))

        self.screen.blit(self.coin_icon, (22, 24))
        score_text = self.font.render(f"Coins:{self.coins_collected}", True, (0, 0, 0))
        self.screen.blit(score_text, (70, 35))

        self.screen.blit(self.time_icon, (680, 30))
        time_text = self.font.render(f"Time:{self.time_left}s", True, (0, 0, 0))
        self.screen.blit(time_text, (730, 35))

        self.screen.blit(self.diamond_icon, (310, 24))
        diamond_text = self.font.render(f"Diamonds:{self.diamonds_collected}", True, (0, 0, 0))
        self.screen.blit(diamond_text, (370, 35))

        self.death_popup.draw()
        pygame.display.update()

    def run(self, event=None):
        if event:
            if self.death_popup.handle_event(event):
                self.__init__(self.screen, self.username)
                return
            
        if not self.death_popup.active:
            self.handle_input()
            self.update_physics()
       
        self.draw()


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


    def _load_single_image(self, path):
        image = pygame.image.load(path).convert_alpha()  # 使用透明通道加载图片
        image.set_colorkey((0, 255, 255))  # 设置青色为透明（0, 255, 255）
        return image
    
    def update_camera(self):
        player_center_x = self.player_rect.centerx
        screen_width = self.screen.get_width()
        self.camera_x = max(0, min(self.world_width - screen_width, player_center_x - screen_width // 2))

    def world_to_screen(self, rect):
        return rect.move(-self.camera_x, 0)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.player_rect.x = max(0, self.player_rect.x - self.player_speed)  # 限制最小x为0，防止超出屏幕左侧
            self.facing_right = False

        if keys[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed
            self.facing_right = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            self.jump_sound.play()

    def update_physics(self):
        current_time = pygame.time.get_ticks()
        if self.state == "playing" and current_time - self.last_time_update > 1000:
            self.time_left -= 1
            self.last_time_update = current_time
            if self.time_left <= 0:
                self.death_popup.show("Time's up! Game over!")
                return
        
        for coin in self.coins:
            coin["frame"] += coin["animation_speed"]
            if coin["frame"] >= len(self.coin_frames):
                coin["frame"] = 0 

        for coin in self.coins[:]: 
            if self.player_rect.colliderect(coin["rect"]):
                self.coins.remove(coin)
                self.coins_collected += 20
                self.score += 20
                self.coin_sound.play()
                
        for diamond in self.diamond[:]: 
            if self.player_rect.colliderect(diamond["rect"]):
                self.diamond.remove(diamond)
                self.diamonds_collected += 10
                self.score += 10
                self.diamond_sound.play()
                
        self.on_ground = False  # 先假设不在地上
        self.velocity_y += self.gravity
        self.player_rect.y += self.velocity_y

        for platform, visible in [
                (self.platform_rect, self.platform_visible),
                (self.platform2_rect, self.platform2_visible),
                (self.platform3_rect, self.platform3_visible),
                (self.platform4_rect, self.platform4_visible),
            ]:
                if visible and self.player_rect.colliderect(platform):
                    if self.velocity_y >= 0:
                        self.player_rect.bottom = platform.top                
                        self.velocity_y = 0
                        self.on_ground = True


        if self.player_rect.colliderect(self.spring.rect):
            if self.player_rect.bottom <= self.spring.rect.top + 20:
                if not self.spring.pressed:
                    self.spring.pressed = True
                    self.spring.image = self.spring_pressed
                    self.velocity_y = -20
                    self.jump_sound.play()
        else:
            self.spring.pressed = False
            self.spring.image = self.spring_normal

        
        for start_x, width, y in self.generate_ground_segments():
            ground_rect = pygame.Rect(start_x, y, width, 100)
            if self.player_rect.colliderect(ground_rect):
                if start_x == 2000:
                    if not any(self.player_rect.colliderect(spike_rect) for spike_rect in [
                        self.spike1_rect, self.spike2_rect, self.spike3_rect, 
                        self.spike4_rect, self.spike5_rect, self.spike6_rect,
                        self.spike7_rect, self.spike8_rect, self.spike9_rect,
                    ]):
                        self.death_popup.show("Please be advised not to place trust in any spike!")
                        return
                self.on_ground = True
                self.player_rect.bottom = ground_rect.top
                self.velocity_y = 0
                break

        # 检查按钮点击
        if self.button.check_player_collision(self.player_rect):
            self.platform_visible = True  # 按钮被点击后，显示平台

        if self.button2.check_player_collision(self.player_rect):
            self.platform2_visible = True
            self.platform3_visible = True
            self.platform4_visible = True

        if self.player_rect.colliderect(self.spike_rect) and self.player_rect.centerx < 2000:
            self.death_popup.show("Caution! You have been slain by deadly spikes!")
            return
            
        if not self.spike_visible:  # 如果还没出现
           distance_to_spike = abs(self.player_rect.centerx - self.spike_rect.centerx)
           if distance_to_spike < 150:
               self.spike_visible = True

        # 玩家是否跌落，重置
        if self.player_rect.bottom > self.screen_height:
            self.death_popup.show("You fell down!")
            return
            

        for fireball in self.fireballs:
            fireball["rect"].x -= fireball["speed"]  # 火球往左飞
   
            # 如果火球飞出画面左侧，就重新生成它（无限循环）
            if fireball["rect"].right < 0:
                fireball["rect"].x = random.randint(1000, 3000)
                fireball["rect"].y = random.randint(200, 400)
                fireball["speed"] = random.randint(3, 6)
       
    # 玩家被火球碰到就重新开始
            if self.player_rect.colliderect(fireball["rect"]):
                self.death_popup.show("Boom! A fireball hits you with searing heat!")
                return


        self.update_camera()
        self.animation_frame += self.animation_speed


    def update(self, dt):
        # Update portal animation
        self.portal_frame_timer += dt
        if self.portal_frame_timer > 100:
            self.portal_frame_index = (self.portal_frame_index + 1) % len(self.portal_frames)
            self.portal_frame_timer = 0

        # Level completed logic
        if self.player_rect.colliderect(self.portal_rect):
            if self.state != "next_level":
                print("Both Mini Game Completed!")
                self.time_used = pygame.time.get_ticks() - self.level_start_time
                self.state = "next_level"

                save_game2_data(
                    username=self.username,
                    coin=self.coins_collected,
                    diamond=self.diamonds_collected,
                    #time_taken=self.time_used / 1000
                )

                
    def update_camera(self):
        player_center_x = self.player_rect.centerx
        screen_width = self.screen.get_width()

        self.camera_x = max(0, min(self.world_width - screen_width, player_center_x - screen_width // 2))

    def generate_ground_segments(self):
        # 地面区段，返回多个地面段的位置和宽度
        return [
            (0,300,600),    # 1st ground
            (700, 500,600),  # 2nd ground
            (2000,530,600),  # 3rd ground
            (2800,400,300)   # 4th ground
        ]

    def get_player_image(self):
        if not self.on_ground:  # 如果不在地面上，显示跳跃动画
            return self.player_images['jump']
        elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            frame_index = int(self.animation_frame) % len(self.player_images['walk'])
            return self.player_images['walk'][frame_index]
        else:
            return self.player_images['idle']

    def draw(self):
        self.screen.blit(self.background, (-self.camera_x, 0))

        for coin in self.coins:
            frame_index = int(coin["frame"]) % len(self.coin_frames)
            image = self.coin_frames[frame_index]
            pos = self.world_to_screen(coin["rect"])
            self.screen.blit(image, pos)
            
        for diamond in self.diamond:
            self.screen.blit(self.diamond_icon, self.world_to_screen(diamond["rect"]))
    
        # 绘制每个地面区段
        for start_x, width, y in self.generate_ground_segments():
            if width > 0:
                ground_surface = self.ground_image_full.subsurface((start_x, 0, width, 100))
                ground_rect = pygame.Rect(start_x, y, width, 100)
                screen_pos = self.world_to_screen(ground_rect)
                self.screen.blit(ground_surface, screen_pos)

        for fireball in self.fireballs:
            self.screen.blit(self.fireball_image, self.world_to_screen(fireball["rect"]))

        # 绘制按钮
        self.button.draw(self.screen, self.camera_x)
        self.button2.draw(self.screen, self.camera_x)

        if self.spike_visible:
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike1_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike2_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike3_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike4_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike5_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike6_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike7_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike8_rect))
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike9_rect))

        # 只有按钮被点击后才绘制平台
        if self.platform_visible:
            self.screen.blit(self.platform_image, self.world_to_screen(self.platform_rect))
        if self.platform2_visible:
            self.screen.blit(self.platform2_image, self.world_to_screen(self.platform2_rect))
        if self.platform3_visible:
            self.screen.blit(self.platform3_image, self.world_to_screen(self.platform3_rect))
        if self.platform4_visible:
            self.screen.blit(self.platform4_image, self.world_to_screen(self.platform4_rect))

        portal_frame = self.portal_frames[self.portal_frame_index]
        self.screen.blit(portal_frame, self.world_to_screen(self.portal_rect))


        # 绘制玩家
        current_image = self.get_player_image()  # 处理玩家面向方向
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        self.screen.blit(current_image, self.world_to_screen(self.player_rect))

        self.screen.blit(self.spring.image, self.world_to_screen(self.spring.rect))

        ui_bar = pygame.Surface((380, 50), pygame.SRCALPHA)
        self.screen.blit(ui_bar, (20, 20))

        self.screen.blit(self.coin_icon, (22, 24))
        score_text = self.font.render(f"Coins:{self.coins_collected}", True, (0, 0, 0))
        self.screen.blit(score_text, (70, 35))

        self.screen.blit(self.time_icon, (680, 30))
        time_text = self.font.render(f"Time:{self.time_left}s", True, (0, 0, 0))
        self.screen.blit(time_text, (730, 35))

        self.screen.blit(self.diamond_icon, (310, 24))
        diamond_text = self.font.render(f"Diamonds:{self.diamonds_collected}", True, (0, 0, 0))
        self.screen.blit(diamond_text, (370, 35))

        self.death_popup.draw()
        pygame.display.update()

    def run(self, event=None):
        if event:
            if self.death_popup.handle_event(event):
                self.__init__(self.screen, self.username)
                return
            
        if not self.death_popup.active:
            dt = self.clock.tick(60)
            self.update(dt)
            self.handle_input()
            self.update_physics()
            self.update_camera()

        self.draw()'''


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

class Game1:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.SysFont('Arial', 32)
        self.has_printed_success = False 
        self.world_width = 3200
        self.camera_x = 0
        self.state = "playing"
        self.score = 0
        self.time_left = 30
        self.last_time_update = pygame.time.get_ticks()
        self.portal_frame_index = 0 
        self.portal_animation_speed = 0.2
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 27)

        self.level_start_time = pygame.time.get_ticks()
        self.time_used = 0

        self.coins_collected = 0
        self.diamonds_collected = 0

        self.coin_icon = pygame.image.load("assets/images/ui/coin_icon.png").convert_alpha()
        self.time_icon = pygame.image.load("assets/images/ui/time_icon.png").convert_alpha()
        self.diamond_icon = pygame.image.load("assets/images/ui/diamond_icon.png").convert_alpha()
        self.dian_image = pygame.image.load("assets/images/dian.png").convert_alpha()

        self.jump_sound = pygame.mixer.Sound('assets/sounds/player_jump.wav')
        self.jump_sound.set_volume(0.2)
        self.dian_sound = pygame.mixer.Sound("assets/sounds/dian.wav") 
        self.dian_sound.set_volume(2.0)
        self.diamond_sound = pygame.mixer.Sound("assets/sounds/diamond.wav")
        self.diamond_sound.set_volume(4.0)
        self.coin_sound = pygame.mixer.Sound('assets/sounds/coin.wav')
        self.coin_sound.set_volume(0.3)

        self.death_popup = DeathPopup(screen, self.screen_width, self.screen_height)
        
        self._load_game_assets()

        self.player_rect = self.player_images['idle'].get_rect()
        self.player_rect.midbottom = (140, 70)
        self.player_speed = 5
        self.velocity_y = 0
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        self.animation_speed = 0.15

        self.split_positions = [1000, 2500]
        self.split_progresses = [0 for _ in self.split_positions]
        self.split_width = 220
        self.ground_split_flags = [False for _ in self.split_positions]

        self.coins = []
        for _ in range(12):         
            x = random.randint(100, self.world_width - 100)
            y = random.randint(300, 495)
            coin_rect = pygame.Rect(x, y, 30, 30)
            self.coins.append({
                "rect": coin_rect,
                "frame": 0,
                "animation_speed": 0.2
            })

        self.diamond = []
        for _ in range(5):  
            x = random.randint(100, self.world_width - 100)
            y = random.randint(300, 495)
            diamond_rect = pygame.Rect(x, y, 30, 30)
            self.diamond.append({
                "rect": diamond_rect
            })

        self.portal_frames = []
        for i in range(16):
            frame = pygame.image.load(f"assets/images/portal/portal_{i}.png").convert_alpha()
            self.portal_frames.append(frame)

        self.dians = [
            {"rect": pygame.Rect(450, 500, 40, 40), "collected": False},   
            {"rect": pygame.Rect(620, 500, 40, 40), "collected": False},  
            {"rect": pygame.Rect(790, 500, 40, 40), "collected": False},  
        ]

        self.bricks = [
            {"rect": pygame.Rect(350, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1600, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1850, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1890, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(2800, 585, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(3100, 521, 40, 40), "type": "portal", "active": True}
        ]

    def _load_game_assets(self):

        sky = pygame.image.load("assets/images/level1_background.png").convert()
        sky = pygame.transform.smoothscale(sky, (self.screen_width, self.screen_height))

        self.background = pygame.Surface((self.world_width, self.screen_height))
        for x in range(0, self.world_width, self.screen_width):
            self.background.blit(sky, (x, 0))

        self.ground_image_full = pygame.image.load("assets/images/ground.png").convert_alpha()
        self.ground_image_full = pygame.transform.smoothscale(self.ground_image_full, (self.world_width, 100))

        self._placeholder = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self._placeholder, (255, 0, 255), (0, 0, 32, 32))
        
        self.player_images = {
            'idle': self._load_single_image("assets/images/player/player_stand.png"),
            'walk': [
                self._load_single_image("assets/images/player/player_walk1.png"),
                self._load_single_image("assets/images/player/player_walk2.png")
                ],
            'jump': self._load_single_image("assets/images/player/player_stand.png")
        }

        self.coin_frames = [
            self._load_single_image("assets/images/coin/coin_frame_1.png"),
            self._load_single_image("assets/images/coin/coin_frame_2.png"),
            self._load_single_image("assets/images/coin/coin_frame_3.png"),
            self._load_single_image("assets/images/coin/coin_frame_4.png"),
            self._load_single_image("assets/images/coin/coin_frame_5.png"),
            self._load_single_image("assets/images/coin/coin_frame_6.png"),
        ]

        self.spike_image = self._load_single_image("assets/images/spike.png")


    def _load_single_image(self, path):
        image = pygame.image.load(path).convert_alpha()  # 使用透明通道加载图片
        image.set_colorkey((0, 255, 255))  # 设置青色为透明（0, 255, 255）
        return image
    
    def update_camera(self):
        target_x = self.player_rect.centerx - self.screen_width // 2
        self.camera_x = max(0, min(target_x, self.world_width - self.screen_width))

    def world_to_screen(self, rect):
        return rect.move(-self.camera_x, 0)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= self.player_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed
            self.facing_right = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            self.jump_sound.play()

    # time setting
    def update_physics(self):
        current_time = pygame.time.get_ticks()
        
        if self.state == "playing" and current_time - self.last_time_update > 1000:
            self.time_left -= 1
            self.last_time_update = current_time
            if self.time_left <= 0:
                self.death_popup.show("Time's up! Game over!")
                return
        
        self.velocity_y += self.gravity
        self.player_rect.y += self.velocity_y
        self.portal_frame_index += self.portal_animation_speed
        if self.portal_frame_index >= len(self.portal_frames):
           self.portal_frame_index = 0

        for coin in self.coins:
            coin["frame"] += coin["animation_speed"]
            if coin["frame"] >= len(self.coin_frames):
                coin["frame"] = 0 

        for coin in self.coins[:]: 
            if self.player_rect.colliderect(coin["rect"]):
                self.coins.remove(coin)
                self.coins_collected += 20
                self.score += 20
                self.coin_sound.play()
                
        for diamond in self.diamond[:]: 
            if self.player_rect.colliderect(diamond["rect"]):
                self.diamond.remove(diamond)
                self.diamonds_collected += 10 
                self.score += 10
                self.diamond_sound.play()
                                   
        #ground material        
        for i, pos in enumerate(self.split_positions):
            if not self.ground_split_flags[i] and abs(self.player_rect.centerx - pos) < 200:
                self.ground_split_flags[i] = True
            if self.ground_split_flags[i] and self.split_progresses[i] < self.split_width:
                self.split_progresses[i] += 22 # the speed of open the ground

        self.on_ground = False
        for start_x, width in self.generate_ground_segments():
            ground_rect = pygame.Rect(start_x, 605, width, 100)
            if self.player_rect.colliderect(ground_rect):
                self.on_ground = True
                self.player_rect.bottom = ground_rect.top
                self.velocity_y = 0
                break

        for index, dian in enumerate(self.dians):
            if not dian["collected"] and self.player_rect.colliderect(dian["rect"]):
                if index == 1:
                    self.death_popup.show("Please be advised not to place trust in any ball!")
                    return
                else:
                    dian["collected"] = True
                    self.dian_sound.play()
               
        if self.player_rect.bottom > self.screen_height:
            self.death_popup.show("You fell off the ground!")
            return
        
        for brick in self.bricks:
            if brick["type"] == "spike" and brick["active"]:
                if not brick.get("visible", False):
                    if abs(self.player_rect.centerx - brick["rect"].centerx) < 80:
                        brick["visible"] = True
                        brick["rect"].y -= 30

        for brick in self.bricks:
            if brick["type"] == "spike" and brick["active"]:
                if self.player_rect.colliderect(brick["rect"]):
                    self.death_popup.show("Caution! You have been slain by deadly spikes!")
                    return
                    
        for brick in self.bricks:
            if brick["type"] == "portal" and brick["active"]:
                if self.player_rect.colliderect(brick["rect"]):
                    if self.state != "next_level":
                        self.time_used = pygame.time.get_ticks() - self.level_start_time
                        self.state = "next_level"

                        if not self.has_printed_success:
                           print("Congratulations!")

                           save_game1_data(
                               username=self.username,
                               coin=self.coins_collected,
                               diamond=self.diamonds_collected,
                               #time_taken=self.time_used / 1000
                           )

                           self.has_printed_success = True
                                        
        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(self.world_width, self.player_rect.right)

        self.update_camera()
        self.animation_frame += self.animation_speed

    def generate_ground_segments(self):
        ground_segments = []
        last_x = 0
        for i, pos in enumerate(self.split_positions):
            progress = self.split_progresses[i]
            gap_start = pos - progress // 2
            gap_end = pos + progress // 2

        # 左边的地面段
            if gap_start > last_x:
                ground_segments.append((last_x, gap_start - last_x))  # (起点x, 宽度)

            last_x = gap_end

    # 最后一段地面
        if last_x < self.world_width:
            ground_segments.append((last_x, self.world_width - last_x))

        return ground_segments
    
    def get_player_image(self):
        if not self.on_ground:# if not in ground， run jump photo
            return self.player_images['jump']
        moving = pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]
        if moving:
            frame_index = int(self.animation_frame) % len(self.player_images['walk'])
            return self.player_images['walk'][frame_index]
        return self.player_images['idle']#if not moving anyone, run idle photo

    def draw(self):
        self.screen.blit(self.background, (-self.camera_x, 0))
        # ground crack
        for start_x, width in self.generate_ground_segments():
            if width > 0:
                ground_surface = self.ground_image_full.subsurface((start_x, 0, width, 100))
                self.screen.blit(ground_surface, (start_x - self.camera_x, 600))

        for coin in self.coins:
            frame_index = int(coin["frame"]) % len(self.coin_frames)
            image = self.coin_frames[frame_index]
            self.screen.blit(image, self.world_to_screen(coin["rect"]))

        for diamond in self.diamond:
            self.screen.blit(self.diamond_icon, self.world_to_screen(diamond["rect"]))
           
        for brick in self.bricks:
            if not brick["active"]:
                continue
            if brick["type"] == "spike" and brick.get("visible", False):
                self.screen.blit(self.spike_image, self.world_to_screen(brick["rect"]))
            elif brick["type"] == "portal" and brick["active"]:
                frame_index = int(self.portal_frame_index) % len(self.portal_frames)
                frame = self.portal_frames[frame_index]
                self.screen.blit(frame, self.world_to_screen(brick["rect"]))

        for dian in self.dians:
            if not dian["collected"]:
                self.screen.blit(self.dian_image, self.world_to_screen(dian["rect"]))
                
        current_image = self.get_player_image()# talking about the player face, when the player turn right face follow right.
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        self.screen.blit(current_image, self.world_to_screen(self.player_rect))
       
        ui_bar = pygame.Surface((380, 50), pygame.SRCALPHA)
        self.screen.blit(ui_bar, (20, 20))

        self.screen.blit(self.coin_icon, (22, 24))
        score_text = self.font.render(f"Coins:{self.coins_collected}", True, (0, 0, 0))
        self.screen.blit(score_text, (70, 35))

        self.screen.blit(self.time_icon, (680, 30))
        time_text = self.font.render(f"Time:{self.time_left}s", True, (0, 0, 0))
        self.screen.blit(time_text, (730, 35))

        self.screen.blit(self.diamond_icon, (310, 24))
        diamond_text = self.font.render(f"Diamonds:{self.diamonds_collected}", True, (0, 0, 0))
        self.screen.blit(diamond_text, (370, 35))

        self.death_popup.draw()
        pygame.display.update()

    def run(self, event=None):
        if event:
            if self.death_popup.handle_event(event):
                self.__init__(self.screen, self.username)
                return
            
        if not self.death_popup.active:
            self.handle_input()
            self.update_physics()
       
        self.draw()



