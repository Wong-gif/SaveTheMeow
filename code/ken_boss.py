import pygame
import sys
import os
import random

WIDTH, HEIGHT = 1200, 800
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

fireball_img = pygame.image.load(os.path.join("assets", "images", "fireball.gif")).convert_alpha()
fireball_img = pygame.transform.scale(fireball_img, (30, 30))
 

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.centery = HEIGHT/2
        self.speedy = 10
        self.health = 100


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

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 60))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = HEIGHT/2
        self.speed = random.choice([-2, 2])
        self.shoot_chance = 10
    
    def update(self):
        self.rect.y += self.speed

        if self.rect.top == 0 or self.rect.bottom == HEIGHT:
            self.speed *= -1

        if random.randint(1, 100) <= self.shoot_chance:
            self.shoot()

    def shoot(self):
        fireball = Fireball(self.rect.x, self.rect.y)
        all_sprites.add(fireball)
        fireballs.add(fireball)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = fireball_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.hit_count = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    


all_sprites = pygame.sprite.Group()
fireballs = pygame.sprite.Group()
bullets =  pygame.sprite.Group()
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mario.shoot(  )
    

    all_sprites.update()
    for bullet in bullets:
        hit_fireballs = pygame.sprite.spritecollide(bullet, fireballs, False)
        for fireball in hit_fireballs:
            bullet.kill()  # Remove bullet on hit
            fireball.hit_count += 1  
            if fireball.hit_count >= 5:
                fireball.kill()

    hits = pygame.sprite.spritecollide(mario, fireballs, True)
    for hit in hits:
        mario.health -= 10
        if mario.health <= 0:
            running = False
    

    all_sprites.draw(screen)
    pygame.display.update()



pygame.quit()
sys.exit()
