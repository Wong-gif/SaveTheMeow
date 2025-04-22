import pygame
import random
import os

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.SysFont('Arial', 24)
        self.has_printed_success = False 
        self.world_width = 3200
        self.camera_x = 0
        self.state = "playing"
        self.score = 0
        self.time_left = 60
        self.last_time_update = pygame.time.get_ticks()

        self.coin_sound = pygame.mixer.Sound('assets/sounds/coin.wav')
        self.coin_sound.set_volume(0.3)

        self._load_game_assets()

        self.player_rect = self.player_images['idle'].get_rect()
        self.player_rect.midbottom = (100, 400)
        self.player_speed = 5
        self.velocity_y = 0
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        self.animation_speed = 0.15

        self.split_positions = [1000, 3000]
        self.split_progresses = [0 for _ in self.split_positions]
        self.split_width = 220
        self.ground_split_flags = [False for _ in self.split_positions]

        self.coins = []
        for _ in range(10):         
            x = random.randint(100, self.world_width - 100)
            y = random.randint(100, 400)
            coin_rect = pygame.Rect(x, y, 30, 30)
            self.coins.append({
                "rect": coin_rect,
                "angle": 0,
                "rotation_speed": random.uniform(1, 3),
            })

        self.bricks = [
            {"rect": pygame.Rect(400, 400, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1600, 400, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1850, 400, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(1900, 400, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(2800, 400, 40, 30), "type": "spike", "active": True, "visible": False},
            {"rect": pygame.Rect(3000, 355, 80, 100), "type": "portal", "active": True}
        ]

    def _load_game_assets(self):
        self._placeholder = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self._placeholder, (255, 0, 255), (0, 0, 32, 32))
        
        self.player_images = {
            'idle': self._load_single_image("assets/images/player/player_stand.png"),
            'walk': [self._load_single_image("assets/images/player/player_walk.png")],
            'jump': self._load_single_image("assets/images/player/player_stand.png")
        }
        
        self.spike_image = self._load_single_image("assets/images/spike.png")
        self.coin_image = self._load_single_image("assets/images/coin.png")

    def _load_single_image(self, path):
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Cannot load image: {path}")
            print(f"Error: {e}")
            return self._placeholder

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

    def update_physics(self):
        current_time = pygame.time.get_ticks()
        if self.state == "playing" and current_time - self.last_time_update > 1000:
            self.time_left -= 1
            self.last_time_update = current_time
            if self.time_left <= 0:
                print("time up！game start again。")
                self.__init__(self.screen)

        self.velocity_y += self.gravity
        self.player_rect.y += self.velocity_y


        for coin in self.coins:           
            # 更新旋转角度
            coin["angle"] += coin["rotation_speed"]
            coin["angle"] %= 360
                    
        #ground material
        for i, pos in enumerate(self.split_positions):
            if not self.ground_split_flags[i] and abs(self.player_rect.centerx - pos) < 150:
                self.ground_split_flags[i] = True
            if self.ground_split_flags[i] and self.split_progresses[i] < self.split_width:
                self.split_progresses[i] += 22

        ground_segments = []
        last_x = 0
        for i, pos in enumerate(self.split_positions):
            progress = self.split_progresses[i]
            gap_start = pos - progress // 2
            if gap_start > last_x:
                ground_segments.append(pygame.Rect(last_x, 450, gap_start - last_x, 150))
            last_x = pos + progress // 2
        if last_x < self.world_width:
            ground_segments.append(pygame.Rect(last_x, 450, self.world_width - last_x, 150))

        self.on_ground = False
        for ground in ground_segments:
            if self.player_rect.colliderect(ground):
                self.on_ground = True
                self.player_rect.bottom = ground.top
                self.velocity_y = 0
                break

        if self.player_rect.bottom > self.screen_height:
            print("fall down, game start again")
            self.__init__(self.screen)

        for coin in self.coins[:]:
            if self.player_rect.colliderect(coin["rect"]):
                self.coins.remove(coin)
                self.score += 2
                self.coin_sound.play()

        for brick in self.bricks:
            if brick["type"] == "spike" and brick["active"] and not brick.get("visible", False):
                if abs(self.player_rect.centerx - brick["rect"].centerx) < 80:
                    brick["visible"] = True
                    brick["rect"].y -= 30

        for brick in self.bricks:
            if brick["type"] == "spike" and brick.get("visible", False):
                if self.player_rect.colliderect(brick["rect"]):
                    print("Beware of traps！")
                    self.__init__(self.screen)

        for brick in self.bricks:
            if brick["type"] == "portal" and brick["active"]:
                if self.player_rect.colliderect(brick["rect"]):
                    self.state = "won"
                    if not self.has_printed_success:
                        print("Congratulations on completing the game！")
                        self.has_printed_success = True
                                        

        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(self.world_width, self.player_rect.right)

        self.update_camera()
        self.animation_frame += self.animation_speed

    def get_player_image(self):
        if not self.on_ground:# if not in ground run jump photo
            return self.player_images['jump']
        moving = pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]
        if moving:
            frame_index = int(self.animation_frame) % len(self.player_images['walk'])
            return self.player_images['walk'][frame_index]
        return self.player_images['idle']#if not moving anyone, run idle photo

    def draw(self):
        self.screen.fill((135, 206, 235))#blue background

        ground_segments = []
        last_x = 0
        for i, pos in enumerate(self.split_positions):
            progress = self.split_progresses[i]
            gap_start = pos - progress // 2
            if gap_start > last_x:
                ground_segments.append(pygame.Rect(last_x, 450, gap_start - last_x, 150))
            last_x = pos + progress // 2
        if last_x < self.world_width:
            ground_segments.append(pygame.Rect(last_x, 450, self.world_width - last_x, 150))

        for ground in ground_segments:
            pygame.draw.rect(self.screen, (100, 200, 100), self.world_to_screen(ground))

        for coin in self.coins:
            rotated_image = pygame.transform.rotate(self.coin_image, coin["angle"])
            rotated_rect = rotated_image.get_rect(center=self.world_to_screen(coin["rect"]).center)
            self.screen.blit(rotated_image, rotated_rect)
           

        for brick in self.bricks:
            if not brick["active"]:
                continue
            if brick["type"] == "spike" and brick.get("visible", False):
                self.screen.blit(self.spike_image, self.world_to_screen(brick["rect"]))
            elif brick["type"] == "portal":
                pygame.draw.rect(self.screen, (0, 255, 255), self.world_to_screen(brick["rect"]))

        current_image = self.get_player_image()
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        self.screen.blit(current_image, self.world_to_screen(self.player_rect))

        score_text = self.font.render(f"score: {self.score}", True, (0, 0, 0))
        time_text = self.font.render(f"time: {self.time_left}s", True, (0, 0, 0))
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(time_text, (20, 50))

        if self.state == "won":
            msg = self.font.render(f"You win! final score: {self.score}", True, (0, 0, 0))
            self.screen.blit(msg, (self.screen_width // 2 - 150, self.screen_height // 2))

    def run(self):
        self.handle_input()
        self.update_physics()
        self.draw()
