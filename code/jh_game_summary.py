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

