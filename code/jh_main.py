import pygame
import sys
from jh_level import Level

# pygame and mix the sound
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Save The Meow")
clock = pygame.time.Clock()

MENU = 0
GAME = 1
current_state = MENU

# 尝试加载背景和音乐（添加错误处理）
try:
    background = pygame.image.load('assets/images/background.png').convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    print("cannot load the image")
    
try:
    pygame.mixer.music.load("assets/sounds/background_music.mp3")
    pygame.mixer.music.set_volume(0.5)
except:
    print("cannot play the sound")

# 初始化关卡
level = Level(screen)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)#position
        self.text = text
        self.font = pygame.font.SysFont('Arial', 32)
        self.normal_color = GREEN
        self.hover_color = DARK_GREEN
    
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.normal_color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

start_button = Button(
    SCREEN_WIDTH//2 - 100, 
    SCREEN_HEIGHT//2 + 70, 
    200, 60, 
    "Start The Game"
)

# 主游戏循环
running = True
while running:
    clock.tick(FPS)
    
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
        if current_state == MENU:
            if start_button.is_clicked(event):
                current_state = GAME
                try:
                    pygame.mixer.music.play(-1)  # music start
                except:
                    pass 
    
    # 状态渲染
    if current_state == MENU:
        # 绘制菜单
        screen.blit(background, (0, 0))
        start_button.draw(screen)
    elif current_state == GAME:
        # 运行游戏逻辑
        level.run()
    
    pygame.display.update()

pygame.quit()
sys.exit()