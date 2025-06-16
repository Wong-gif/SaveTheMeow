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
        
        self.portal_rect = pygame.Rect(3100, 221, 80, 100)  # position of portal  
        self.portal_frames = []
        for i in range(16):
            frame = pygame.image.load(f"assets/images/portal/portal_{i}.png").convert_alpha()
            self.portal_frames.append(frame)   

        self.portal_frame_index = 0
        self.portal_frame_timer = 0
        self.level_start_time = pygame.time.get_ticks()     

        self.fireballs = []  
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
        image = pygame.image.load(path).convert_alpha()  
        image.set_colorkey((0, 255, 255)) 
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
            self.player_rect.x = max(0, self.player_rect.x - self.player_speed)  
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
                
        self.on_ground = False 
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
                        self.player_rect.bottom = platform.top # let the player can stand on the platform               
                        self.velocity_y = 0 # stop to fell down
                        self.on_ground = True # can stand and can jump


        if self.player_rect.colliderect(self.spring.rect):
            if self.player_rect.bottom <= self.spring.rect.top + 20: # make sure is jump, not besides jump
                if not self.spring.pressed:
                    self.spring.pressed = True
                    self.spring.image = self.spring_pressed
                    self.velocity_y = -20 # negative means player jump up
                    self.jump_sound.play() # play the sound
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

        # check the button
        if self.button.check_player_collision(self.player_rect):
            self.platform_visible = True  # button click, platform out 

        if self.button2.check_player_collision(self.player_rect):
            self.platform2_visible = True
            self.platform3_visible = True
            self.platform4_visible = True

        if self.player_rect.colliderect(self.spike_rect) and self.player_rect.centerx < 2000:
            self.death_popup.show("Caution! You have been slain by deadly spikes!")
            return
            
        if not self.spike_visible:  # if haven not come out 
           distance_to_spike = abs(self.player_rect.centerx - self.spike_rect.centerx)
           if distance_to_spike < 150:
               self.spike_visible = True

        # player fell down , restart the game 
        if self.player_rect.bottom > self.screen_height:
            self.death_popup.show("You fell down!")
            return
            

        for fireball in self.fireballs:
            fireball["rect"].x -= fireball["speed"]  # fire will fly to the left
   
            # if fire fly out the left screen, it will loop again
            if fireball["rect"].right < 0:
                fireball["rect"].x = random.randint(1000, 3000)
                fireball["rect"].y = random.randint(200, 400)
                fireball["speed"] = random.randint(3, 6)
       
            if self.player_rect.colliderect(fireball["rect"]):
                self.death_popup.show("Boom! A fireball hits you with searing heat!")
                return


        self.update_camera()
        self.animation_frame += self.animation_speed


    def update(self, dt): # delta time = dt
        # Update portal animation
        self.portal_frame_timer += dt # record the time if > o.1 second loop again
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
        return [
            (0,300,600),    # 1st ground
            (700, 500,600),  # 2nd ground
            (2000,530,600),  # 3rd ground
            (2800,400,300)   # 4th ground
        ]

    def get_player_image(self):
        if not self.on_ground: 
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
    
        # draw the ground        
        for start_x, width, y in self.generate_ground_segments(): # this game 2 got many position of ground > ============ > =====      ======
            if width > 0:
                ground_surface = self.ground_image_full.subsurface((start_x, 0, width, 100))
                ground_rect = pygame.Rect(start_x, y, width, 100)
                screen_pos = self.world_to_screen(ground_rect) # camera move , player also move
                self.screen.blit(ground_surface, screen_pos)

        for fireball in self.fireballs:
            self.screen.blit(self.fireball_image, self.world_to_screen(fireball["rect"]))

        
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

        # only button click out , platform will come out 
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


        
        current_image = self.get_player_image()  # about face of the player ( left or right )
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

        self.draw()

