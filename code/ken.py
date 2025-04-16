import pygame
import sys

WIDTH, HEIGHT = 800, 400
BLACK = (0, 0, 0)
LAVA = (255, 69, 0)  #bottom
WHITE = (255, 255, 255)
RED = (255, 0, 0)   #mario
ORANGE = (255, 165, 0)   #boss
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario vs Boss")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)


class Mario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 250

boss = pygame.Rect(700, 250, 60, 60)

all_sprites = pygame.sprite.Group()
mario = Mario()
all_sprites.add(mario)

# Game loop
running = True


while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.draw(screen)
    pygame.display.update()



pygame.quit()
sys.exit()
