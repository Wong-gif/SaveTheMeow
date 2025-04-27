import pygame
import os

class Button:
    def __init__(self, normal_image, pressed_image, x, y):
        self.normal_image = normal_image
        self.pressed_image = pressed_image
        self.image = self.normal_image  # 默认是normal状态
        self.world_x = x
        self.world_y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.world_x - camera_x, self.world_y))

    def check_player_collision(self, player_rect):
        # 用世界坐标的rect检测碰撞
        self.rect.topleft = (self.world_x, self.world_y)
        if self.rect.colliderect(player_rect):
            self.image = self.pressed_image
            return True
        return False

   
class NextLevel:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.world_width = 3200 
        self.camera_x = 0
        self.score = 0
        self.time_left = 60
        self.last_time_update = pygame.time.get_ticks()
        self.spike_image = pygame.image.load("assets/images/spike.png").convert_alpha()
        self.spike_visible = False # make the spike cannot see first
        self.spike_rect = self.spike_image.get_rect()
        self.spike_rect.topleft = (830, 555)  # Place spike in the second ground

        self._load_game_assets()
        self.player_rect = self.player_images['idle'].get_rect()
        self.player_rect.midbottom = (180, 70)  # player position
        self.player_speed = 5
        self.velocity_y = 0
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        self.animation_speed = 0.15

        self.button_normal = pygame.image.load("assets/images/button_normal.png").convert_alpha()
        self.button_pressed = pygame.image.load("assets/images/button_pressed.png").convert_alpha()
        self.button = Button(self.button_normal, self.button_pressed, 0, self.screen_height - 250)

        self.platform_image = pygame.image.load("assets/images/rui.png").convert_alpha()
        self.platform_rect = self.platform_image.get_rect()
        self.platform_rect.midbottom = (490, 500)  # platform position
        self.platform_visible = False  # same as the top, cannot see first

    def _load_game_assets(self):
        sky = pygame.image.load("assets/images/level2_background.png").convert()
        sky = pygame.transform.smoothscale(sky, (3200, self.screen_height))
        self.background = sky

        self.ground_image_full = pygame.image.load("assets/images/platform.png").convert_alpha()
        self.ground_image_full = pygame.transform.smoothscale(self.ground_image_full, (self.world_width, 100))

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
        target_x = self.player_rect.centerx - self.screen_width // 2
        self.camera_x = max(0, min(target_x, self.world_width - self.screen_width))

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

    def update_physics(self):
        self.velocity_y += self.gravity
        self.player_rect.y += self.velocity_y

        # 玩家是否在地面上
        self.on_ground = False
        for start_x, width in self.generate_ground_segments():
            ground_rect = pygame.Rect(start_x, 605, width, 100)
            if self.player_rect.colliderect(ground_rect):
                self.on_ground = True
                self.player_rect.bottom = ground_rect.top
                self.velocity_y = 0
                break

        if self.platform_visible and self.player_rect.colliderect(self.platform_rect):
            self.on_ground = True
            self.player_rect.bottom = self.platform_rect.top  # 玩家站在平台上
            self.velocity_y = 0  # 停止垂直运动

        # 检查按钮点击
        if self.button.check_player_collision(self.world_to_screen(self.player_rect)):
            self.platform_visible = True  # 按钮被点击后，显示平台

        if self.player_rect.colliderect(self.spike_rect):
            print("Beware of traps")
            self.__init__(self.screen)

        # 玩家是否跌落，重置
        if self.player_rect.bottom > self.screen_height:
            print("Fall Down, Game Start Again")
            self.__init__(self.screen)
            
        if not self.spike_visible:  # 如果还没出现
           distance_to_spike = abs(self.player_rect.centerx - self.spike_rect.centerx)
           if distance_to_spike < 150:
               self.spike_visible = True
               
        self.update_camera()
        self.animation_frame += self.animation_speed

    def generate_ground_segments(self):
        # 地面区段，返回多个地面段的位置和宽度
        return [
            (0, 300),    # 第一段
            (700, 500),  # 第二段
        ]

    def get_player_image(self):
        if not self.on_ground:  # 如果不在地面上，显示跳跃动画
            return self.player_images['jump']
        moving = pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]
        if moving:
            frame_index = int(self.animation_frame) % len(self.player_images['walk'])
            return self.player_images['walk'][frame_index]
        return self.player_images['idle']  # 如果不移动，显示站立动画

    def draw(self):
        self.screen.blit(self.background, (-self.camera_x, 0))
    
        # 绘制每个地面区段
        for start_x, width in self.generate_ground_segments():
            if width > 0:
                ground_surface = self.ground_image_full.subsurface((start_x, 0, width, 100))
                self.screen.blit(ground_surface, (start_x - self.camera_x, 600))

        # 绘制按钮
        self.button.draw(self.screen, self.camera_x)

        if self.spike_visible:
            self.screen.blit(self.spike_image, self.world_to_screen(self.spike_rect))

        # 只有按钮被点击后才绘制平台
        if self.platform_visible:
            self.screen.blit(self.platform_image, self.world_to_screen(self.platform_rect))

        # 绘制玩家
        current_image = self.get_player_image()  # 处理玩家面向方向
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        self.screen.blit(current_image, self.world_to_screen(self.player_rect))

    def run(self):
        self.handle_input()
        self.update_physics()
        self.draw()
