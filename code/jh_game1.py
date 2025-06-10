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
        image = pygame.image.load(path).convert_alpha() 
        image.set_colorkey((0, 255, 255))  #set green 
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

        # left ground
            if gap_start > last_x:
                ground_segments.append((last_x, gap_start - last_x))

            last_x = gap_end

    # last ground
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



