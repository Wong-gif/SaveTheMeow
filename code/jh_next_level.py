import pygame
import os

class NextLevel:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.SysFont('Arial', 32)
        self.camera_x = 0
        self.world_width = 3200  # 可根据地图大小调整

        self._load_assets()

        self.player_rect = self.player_image.get_rect()
        self.player_rect.midbottom = (100, self.screen_height - 100)
        self.player_speed = 5
        self.velocity_y = 0
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True

    def _load_assets(self):
        bg = pygame.image.load("assets/images/abc.png").convert()
        self.background = pygame.Surface((self.world_width, self.screen_height))
        for x in range(0, self.world_width, bg.get_width()):
            scaled_bg = pygame.transform.scale(bg, (bg.get_width(), self.screen_height))
            self.background.blit(scaled_bg, (x, 0))

        # 加载玩家
        self.player_image = pygame.image.load("assets/images/player/player_stand.png").convert_alpha()

        # 加载背景音乐
        try:
            pygame.mixer.music.load("assets/sounds/background.music.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("背景音乐播放失败：", e)

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
        # 简化版，玩家在空气中
        self.velocity_y += self.gravity
        self.player_rect.y += self.velocity_y

        # 碰到底部就站住
        if self.player_rect.bottom >= self.screen_height:
            self.player_rect.bottom = self.screen_height
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        self.update_camera()

    def update_camera(self):
        target_x = self.player_rect.centerx - self.screen_width // 2
        self.camera_x = max(0, min(target_x, self.world_width - self.screen_width))

    def world_to_screen(self, rect):
        return rect.move(-self.camera_x, 0)

    def draw(self):
        self.screen.blit(self.background, (-self.camera_x, 0))

        # 玩家渲染
        image = self.player_image
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        self.screen.blit(image, self.world_to_screen(self.player_rect))

        text = self.font.render("Next Level", True, (0, 0, 0))
        self.screen.blit(text, (20, 20))

    def run(self):
        self.handle_input()
        self.update_physics()
        self.draw()

