import pygame
import os

class NextLevel:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.SysFont('Arial', 32)
        self.camera_x = 0
        self.world_width = 3200  # 世界宽度设置为3200px

        self._load_game_assets()
        self.animation_frame = 0
        self.animation_speed = 0.15

        self.player_rect = self.player_images['idle'].get_rect()
        self.player_rect.midbottom = (100, self.screen_height - 100)
        self.player_speed = 5
        self.velocity_y = 0
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True

        self.platforms = [
            pygame.Rect(100, 600, 300, 30),
            pygame.Rect(600, 500, 300, 30),
            pygame.Rect(1200, 400, 300, 30),
            pygame.Rect(1800, 300, 300, 30),
            pygame.Rect(2500, 600, 400, 30),
        ]

    def _load_game_assets(self):
        # 加载并拉长背景
        bg = pygame.image.load("assets/images/level2_background.png").convert()
        bg = pygame.transform.scale(bg, (self.world_width, self.screen_height))
        self.background = bg

        # 玩家图片
        self.player_images = {
            'idle': self._load_single_image("assets/images/player/player_stand.png"),
            'walk': [
                self._load_single_image("assets/images/player/player_walk1.png"),
                self._load_single_image("assets/images/player/player_walk2.png")
            ],
            'jump': self._load_single_image("assets/images/player/player_stand.png")
        }

        # 地面图
        self.ground_image = pygame.image.load("assets/images/level2_ground.png").convert_alpha()
        self.ground_image = pygame.transform.scale(self.ground_image, (self.world_width, 100))
        self.ground_rect = pygame.Rect(0, self.screen_height - 100, self.world_width, 100)

    def _load_single_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return image

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

        self.player_rect.left = max(0, self.player_rect.left)
        self.player_rect.right = min(self.world_width, self.player_rect.right)

    def update_physics(self):
        self.velocity_y += self.gravity
        self.player_rect.y += self.velocity_y

        self.animation_frame += self.animation_speed

        if self.player_rect.bottom >= self.screen_height - 100:
            self.player_rect.bottom = self.screen_height - 100
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        self.on_ground = False
        for platform in self.platforms:
            if self.player_rect.colliderect(platform) and self.velocity_y >= 0:
                self.player_rect.bottom = platform.top
                self.velocity_y = 0
                self.on_ground = True
                break

        if self.player_rect.top > self.screen_height:
            print("Fall Down! Game Restart")
            self.__init__(self.screen)

    def update_camera(self):
        target_x = self.player_rect.centerx - self.screen_width // 2
        self.camera_x = max(0, min(target_x, self.world_width - self.screen_width))

    def world_to_screen(self, rect):
        return rect.move(-self.camera_x, 0)

    def draw(self):
        self.screen.blit(self.background, (-self.camera_x, 0))
        self.screen.blit(self.ground_image, self.world_to_screen(self.ground_rect))

        for platform in self.platforms:
            pygame.draw.rect(self.screen, (139, 69, 19), self.world_to_screen(platform))

        # 玩家
        if not self.on_ground:
            image = self.player_images['jump']
        else:
            keys = pygame.key.get_pressed()
            moving = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
            if moving:
                frame_index = int(self.animation_frame) % len(self.player_images['walk'])
                image = self.player_images['walk'][frame_index]
            else:
                image = self.player_images['idle']

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        self.screen.blit(image, self.world_to_screen(self.player_rect))

    def run(self):
        self.handle_input()
        self.update_physics()
        self.update_camera()
        self.draw()
