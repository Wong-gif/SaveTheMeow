import pygame

class DeathPopup:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.active = False
        self.reason = ""
        self.restart_button = pygame.Rect(0, 0, 160, 50)
        self.font = pygame.font.SysFont("arial", 28)

    def show(self, reason_text):
        self.active = True
        self.reason = reason_text

    def hide(self):
        self.active = False

    def draw(self):
        if not self.active:
            return

        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        popup_width, popup_height = 500, 300
        popup_x = self.WIDTH // 2 - popup_width // 2
        popup_y = self.HEIGHT // 2 - popup_height // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, border_radius=15)

        reason_text = self.font.render(self.reason, True, (0, 0, 0))
        self.screen.blit(reason_text, (
            popup_x + popup_width // 2 - reason_text.get_width() // 2,
            popup_y + 80
        ))

        self.restart_button = pygame.Rect(popup_x + popup_width // 2 - 80, popup_y + 180, 160, 50)
        pygame.draw.rect(self.screen, (200, 0, 0), self.restart_button, border_radius=8)

        restart_text = self.font.render("Restart", True, (255, 255, 255))
        self.screen.blit(restart_text, (
            self.restart_button.x + self.restart_button.width // 2 - restart_text.get_width() // 2,
            self.restart_button.y + 10
        ))

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                return True
        return False

import pygame

# 初始化pygame
pygame.init()

# 设定屏幕尺寸
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Cover")

# 加载并调整背景图片
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 加载马里奥角色
mario = pygame.image.load("mario.png")
mario = pygame.transform.scale(mario, (100, 100))

# Mario 位置
mario_x = 350
mario_y = 400
mario_speed = 2  # 降低速度
jump = False
jump_height = 10
gravity = jump_height

# 设定字体
font = pygame.font.Font(None, 80)
title_text = font.render("Super Mario", True, (255, 215, 0))

# 剧情文本
story_font = pygame.font.Font(None, 40)
story_text = [
    "once a lot a time ......",
    "help! me ",
    "HAlo！",
    "press ENTER to start the game"
]

# 游戏状态
show_story = True
running = True

while running:
    screen.fill((0, 0, 0))  # 黑色背景
    
    if show_story:
        # 显示剧情文本
        for i, line in enumerate(story_text):
            text_surface = story_font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (100, 150 + i * 50))
    else:
        # 游戏主界面
        screen.fill((135, 206, 250))  # 天空蓝色背景
        screen.blit(background, (0, 0))  # 显示背景
        screen.blit(mario, (mario_x, mario_y))  # 显示马里奥角色
        screen.blit(title_text, (250, 50))  # 显示标题

        # 获取按键状态
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # 左移
            mario_x -= mario_speed
        if keys[pygame.K_RIGHT]:  # 右移
            mario_x += mario_speed
        if keys[pygame.K_SPACE] and not jump:  # 跳跃
            jump = True

        # 处理跳跃逻辑
        if jump:
            mario_y -= gravity  # 向上跳
            gravity -= 1
            if gravity < -jump_height:
                jump = False
                gravity = jump_height
    
    # 监听事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            show_story = False  # 按 Enter 进入游戏

    pygame.display.flip()

pygame.quit()
