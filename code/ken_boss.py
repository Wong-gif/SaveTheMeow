import pygame
import sys
import os
import random
from ken_effect import WeaponEffects

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
pygame.mixer.init()
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 20)

fireball_img = pygame.image.load(os.path.join("assets", "images", "fireball.gif")).convert_alpha()
fireball_img = pygame.transform.scale(fireball_img, (30, 30))
background_img = pygame.image.load(os.path.join("assets", "images", "boss_back.png")).convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, 300))
player_img = pygame.image.load(os.path.join("assets", "images", "playerboss.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (WIDTH, 300))


original_weapon_images = {
    "Thunder Axe": pygame.image.load(os.path.join("assets", "images", "Thunder_axe.png")).convert_alpha(),
    "Essence of Renewal": pygame.image.load(os.path.join("assets", "images", "Essence_renewal.png")).convert_alpha(),
    "Luna Bow": pygame.image.load(os.path.join("assets", "images", "Luna_bow.png")).convert_alpha(),
    "Hydro Strike": pygame.image.load(os.path.join("assets", "images", "Hydro_strike.png")).convert_alpha(),
    "Aegis Shield": pygame.image.load(os.path.join("assets", "images", "Aegis_shield.png")).convert_alpha(),
    "Hawk's Eye": pygame.image.load(os.path.join("assets", "images", "Hawk_eye.png")).convert_alpha(),
    "Lion Sword": pygame.image.load(os.path.join("assets", "images", "Lion_sword.png")).convert_alpha(),
    "Shadow Gilt": pygame.image.load(os.path.join("assets", "images", "Shadow_gilt.png")).convert_alpha(),
    "Phoenix Feather": pygame.image.load(os.path.join("assets", "images", "Phoenix_feather.png")).convert_alpha(),
}

shoot_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "shoot.wav"))
click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click.wav"))    



def draw_health_bar(surf, hp, max_hp, x, y):
    if hp < 0:
        hp = 0
    HEALTH_LENGTH = 100
    HEALTH_HEIGHT = 10
    fill = (hp / max_hp) * HEALTH_LENGTH
    outline_rect = pygame.Rect(x, y, HEALTH_LENGTH, HEALTH_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, HEALTH_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect) #生命线
    pygame.draw.rect(surf, WHITE, outline_rect, 2) #框

 

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (40, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.centery = HEIGHT/2
        self.speedy = 10
        self.health = 100
        self.lives = 3
        self.attack_power = 100  # Normal power
        self.power_timer = 0     # Timer for power-ups
        self.shield = False      # No shield
        self.shield_timer = 0    # Timer for shield
        self.active_weapon = None
        self.activate_message = ""
        self.activate_message_timer = 0
        self.expired_message = ""
        self.expired_message_timer = 0



    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy
        if key_pressed[pygame.K_LEFT]:
           self.rect.x -= self.speedy
        if key_pressed[pygame.K_RIGHT]:
           self.rect.x += self.speedy

        if self.rect.top < 125:
            self.rect.top = 125
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.left < 0:
           self.rect.left = 0
        if self.rect.right > WIDTH:
           self.rect.right = WIDTH

        # Power-up duration check
        if self.power_timer and pygame.time.get_ticks() > self.power_timer:
            self.expired_message = f"{self.active_weapon} effect expired. Attack power back to normal."
            self.expired_message_timer = pygame.time.get_ticks() + 2000
            self.active_weapon = None
            self.attack_power = 100  # reset to normal damage
            self.power_timer = 0
            

        if self.shield_timer and pygame.time.get_ticks() > self.shield_timer:
            self.expired_message = "Aegis Shield effect expired."
            self.expired_message_timer = pygame.time.get_ticks() + 2000
            self.shield = False
            self.shield_timer = 0


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
        
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 100))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = HEIGHT/2
        self.speed = random.choice([-2, 2])
        self.shoot_chance = 5
        self.health = 10000
    
    def update(self):
        self.rect.y += self.speed

        if self.rect.top <= 125 or self.rect.bottom >= HEIGHT:
            self.speed *= -1
            self.speed += random.choice([-1, 0, 1])
            if self.speed == 0:
                self.speed = random.choice([-2, 2])

        if random.randint(1, 100) <= self.shoot_chance:
            self.shoot()

        if self.health < 9000:
            self.shoot_chance = 10


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
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(3, 6)
        self.hit_count = 0

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

weapon_buttons = [] 

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
    #screen.blit(background_img, (0, 500))

    x = 150
    y = 0
    box = pygame.Surface((900, 120), pygame.SRCALPHA)
    box.fill((0, 0, 0, 0))  # Fully transparent base
    pygame.draw.rect(box, (*BLACK, 100), box.get_rect(), border_radius=12)
    screen.blit(box, (x, y))

    x_box = 160
    y_box = 15
    weapon_buttons.clear()
    for weapon_name, img in original_weapon_images.items():      # loop thought the weapon image
        scaled_images = pygame.transform.smoothscale(img, (90, 90))
        img_rect = pygame.Rect(x_box, y_box, 90, 90)
        screen.blit(scaled_images, (x_box, y_box))
        weapon_buttons.append((weapon_name, img_rect)) 
        x_box += 100      # Spacing between images
   
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mario.shoot()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for weapon_name, rect in weapon_buttons:
                if rect.collidepoint(mouse_pos):
                    click_sound.play()
                    # Apply the effect to Mario or Boss here
                    WeaponEffects.apply(weapon_name, mario, boss)
            
    all_sprites.update()
    for bullet in bullets:
        hit_fireballs = pygame.sprite.spritecollide(bullet, fireballs, False)
        for fireball in hit_fireballs:
            bullet.kill()  # Remove bullet on hit
            fireball.hit_count += 1  
            if fireball.hit_count >= 3:
                fireball.kill()

    boss_hits = pygame.sprite.spritecollide(boss, bullets, True)
    for hit in boss_hits:
        boss.health -= mario.attack_power
        if boss.health <= 0:
            boss.kill()
            running = False

           
    
    mario_hits = pygame.sprite.spritecollide(mario, fireballs, True)
    for hit in mario_hits:
        if mario.shield:
            print("Blocked by Aegis Shield!")
            continue  # 没伤害
        mario.health -= 2
        if mario.health <= 0:
            mario.lives -= 1
            running = False

    
    all_sprites.draw(screen)
    draw_health_bar(screen, mario.health, 100, 5, 15)  # Mario HP
    draw_health_bar(screen, boss.health, 10000, boss.rect.x - 20, boss.rect.top - 20)  # Boss HP


    if mario.activate_message and pygame.time.get_ticks() < mario.activate_message_timer:
        msg = font.render(mario.activate_message, True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 60))

    # Show expired weapon message
    if mario.expired_message and pygame.time.get_ticks() < mario.expired_message_timer:
        msg = font.render(mario.expired_message, True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 30))

    pygame.display.update()

pygame.quit()
sys.exit()
