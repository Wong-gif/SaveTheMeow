import pygame
import sys
import random

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
        self.rect.centery = HEIGHT/2
        self.speedy = 10


    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 60))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = HEIGHT/2
        self.speed = random.choice([-2, 2])
    
    def update(self):
        self.rect.y += self.speed

        if self.rect.top == 0 or self.rect.bottom == HEIGHT:
            self.speed *= -1



        

boss = pygame.Rect(700, 250, 60, 60)

all_sprites = pygame.sprite.Group()
mario = Mario()
boss = Boss()
all_sprites.add(mario)
all_sprites.add(boss)

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    all_sprites.draw(screen)
    pygame.display.update()



pygame.quit()
sys.exit()
