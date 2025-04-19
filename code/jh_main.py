import pygame
import sys
from jh_level import Level
import pygame as pg

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Save The Meow")
clock = pygame.time.Clock()

background = pg.image.load('assets/images/background.png').convert()
background = pg.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.set_volume(0.5)

# Game states
MENU = 0
GAME = 1
current_state = MENU

# Initialize level
level = Level(screen)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
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

# Create start button
start_button = Button(
    SCREEN_WIDTH//2 - 100, 
    SCREEN_HEIGHT//2 + 70, 
    200, 60, 
    "Start The Game"
)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if current_state == MENU and start_button.is_clicked(event):
            current_state = GAME
            pygame.mixer.music.play(-1)
    
    if current_state == MENU:
        # Draw menu state - background with button
        screen.blit(background, (0, 0))
        start_button.draw(screen)
    elif current_state == GAME:
        # Draw game state - black screen
        screen.fill(BLACK)
        level.run()
    
    pygame.display.update()

pygame.quit()
sys.exit()