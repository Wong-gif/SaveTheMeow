import pygame
import sys
import os
import random
from ken_effect import WeaponEffects

WIDTH, HEIGHT = 1200, 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 

pygame.init()
pygame.mixer.init()

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("BOSS STAGE")
clock = pygame.time.Clock()

click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click.wav"))

# Game states
MENU = "menu"
BOSS_STAGE = "boss_stage"
current_state = MENU

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)
        self.normal_color = BLACK
        self.hover_color = BLACK
    
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.normal_color

        shadow_offset = 5
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)

        pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=10)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = self.font.render(self.text, True, WHITE)  # Changed text color to WHITE for visibility
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# Create menu button
start_button = Button(
    WIDTH//2 - 250, 
    HEIGHT//2 - 40, 
    500, 80, 
    "Start The Game"
)

def boss_stage():

    RED = (255, 0, 0)   # mario
    ORANGE = (255, 165, 0)   # boss
    GREEN = (0, 255, 0)
    GREY = (200, 200, 200) 

    font = pygame.font.SysFont("arial", 22)

    fireball_img = pygame.image.load(os.path.join("assets", "images", "fireball.gif")).convert_alpha()
    fireball_img = pygame.transform.scale(fireball_img, (30, 30))
    background_img = pygame.image.load(os.path.join("assets", "images", "boss_back.jpg")).convert_alpha()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    player_img = pygame.image.load(os.path.join("assets", "images", "playerboss.png")).convert_alpha()
    bullet_img = pygame.image.load(os.path.join("assets", "images", "bullet.png")).convert_alpha()
    shield_img = pygame.image.load(os.path.join("assets", "images", "shield.png")).convert_alpha()
    shield_img = pygame.transform.smoothscale(shield_img, (60, 60))

    original_weapon_images = {
        "Phoenix Feather": pygame.image.load(os.path.join("assets", "images", "Phoenix_feather.png")).convert_alpha(),
        "Essence of Renewal": pygame.image.load(os.path.join("assets", "images", "Essence_renewal.png")).convert_alpha(),
        "Luna Bow": pygame.image.load(os.path.join("assets", "images", "Luna_bow.png")).convert_alpha(),
        "Hydro Strike": pygame.image.load(os.path.join("assets", "images", "Hydro_strike.png")).convert_alpha(),
        "Aegis Shield": pygame.image.load(os.path.join("assets", "images", "Aegis_shield.png")).convert_alpha(),
        "Hawk's Eye": pygame.image.load(os.path.join("assets", "images", "Hawk_eye.png")).convert_alpha()
    }

    # Load animation frames
    fire_arrow_frames = []
    for i in range(1, 7):
        img = pygame.image.load(os.path.join("assets", "images", "fire_arrow", f"fire_arrow_{i}.png")).convert_alpha()
        img = pygame.transform.scale(img, (90, 30))
        fire_arrow_frames.append(img)

    water_bullet_frames = []
    for i in range(1, 5):
        img = pygame.image.load(os.path.join("assets", "images", "water_bullet", f"water_bullet_{i}.png")).convert_alpha()
        img = pygame.transform.scale(img, (40, 40)) 
        water_bullet_frames.append(img)

    luna_arrow_frames = []
    for i in range(1, 4):
        img = pygame.image.load(os.path.join("assets", "images", "luna_arrow", f"luna_arrow_{i}.png")).convert_alpha()
        img = pygame.transform.scale(img, (60, 60))
        luna_arrow_frames.append(img)

    add_health_frames = []
    for i in range(1, 5):
        img = pygame.image.load(os.path.join("assets", "images", "add_health", f"add_health_{i}.png")).convert_alpha()
        img = pygame.transform.scale(img, (80, 80))
        add_health_frames.append(img)

    hawk_arrow_frames = []
    for i in range(1, 3):
        img = pygame.image.load(os.path.join("assets", "images", "hawk_arrow", f"hawk_arrow_{i}.png")).convert_alpha()
        img = pygame.transform.scale(img, (60, 60)) 
        hawk_arrow_frames.append(img)



    shoot_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "shoot.wav"))
    click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click.wav")) 
    add_health_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "add_health.wav")) 


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
            self.attack_power = random.randint(80, 100)  # Normal power
            self.last_shoot_time = 0
            self.shoot_delay = 100
            self.power_timer = 0     # Timer for power-ups
            self.shield = False      # No shield
            self.shield_timer = 0    # Timer for shield
            self.active_weapon = None
            self.activate_message = ""
            self.activate_message_timer = 0
            self.expired_message = ""
            self.expired_message_timer = 0
            self.bullet_color = BLACK
            self.shield_img = shield_img  # Store the shield image

        def draw_shield(self, screen):
            if self.shield:
                shield_rect = self.shield_img.get_rect(center=self.rect.center)
                screen.blit(self.shield_img, shield_rect)


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
                self.expired_message = f"{self. active_weapon} effect expired. Attack power back to normal."
                self.expired_message_timer = pygame.time.get_ticks() + 2000
                self.active_weapon = None
                self.attack_power = random.randint(80, 100)  # reset to normal
                self.bullet_color = BLACK   # RESET TO NORMAL 
                self.power_timer = 0
                

            if self.shield_timer and pygame.time.get_ticks() > self.shield_timer:
                self.expired_message = "Aegis Shield effect expired."
                self.expired_message_timer = pygame.time.get_ticks() + 2000
                self.shield = False
                self.shield_timer = 0


        def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shoot_time < self.shoot_delay:
                return
            
            self.last_shoot_time = now

            if self.active_weapon == "Phoenix Feather":
                bullet = AnimatedArrowFire(self.rect.centerx, self.rect.centery, fire_arrow_frames)
                all_sprites.add(bullet)
                bullets.add(bullet) 
            elif self.active_weapon == "Hydro Strike":
                bullet = AnimatedBulletHydro(self.rect.centerx, self.rect.centery, water_bullet_frames)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.active_weapon == "Luna Bow":
                bullet = AnimatedArrowLuna(self.rect.centerx, self.rect.centery, luna_arrow_frames)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.active_weapon == "Hawk's Eye":
                bullet = AnimatedArrowHawk(self.rect.centerx, self.rect.centery, hawk_arrow_frames)
                all_sprites.add(bullet)
                bullets.add(bullet)
            else:
                bullet = Bullet(self.rect.centerx, self.rect.centery, self.bullet_color)
                all_sprites.add(bullet)
                bullets.add(bullet)
            shoot_sound.play()
            
    class Boss(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((60, 100))
            self.image.fill(ORANGE)
            self.rect = self.image.get_rect()
            self.rect.x = 1080
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
                self.shoot_chance = 8


        def shoot(self):
            fireball = Fireball(self.rect.x, self.rect.y)
            all_sprites.add(fireball)
            fireballs.add(fireball)


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(bullet_img, (30, 30))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = 5

        def update(self):
            self.rect.x += self.speed
            if self.rect.left > WIDTH:
                self.kill()

    class AnimatedArrowFire(pygame.sprite.Sprite):
        def __init__(self, x, y, frames):
            super().__init__()
            self.frames = frames
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 7
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100

        def update(self):
            # 当他正在动
            self.rect.x += self.speed
            if self.rect.left > WIDTH:
                self.kill()

            
            if pygame.time.get_ticks() - self.last_update > self.frame_rate:
                    self.last_update = pygame.time.get_ticks()
                    self.frame_index = (self.frame_index + 1) % len(self.frames)
                    self.image = self.frames[self.frame_index]

        
    class AnimatedBulletHydro(pygame.sprite.Sprite):
        def __init__(self, x, y, frames):
            super().__init__()
            self.frames = frames
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 7
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100  

        def update(self):
            # 当他正在动
            self.rect.x += self.speed
            if self.rect.left > WIDTH:
                self.kill()

            # 动画
            if pygame.time.get_ticks() - self.last_update > self.frame_rate:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]

    class AnimatedAddHealth(pygame.sprite.Sprite):
        def __init__(self, mario, frames):
            super().__init__()
            self.frames = frames
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.mario = mario
            self.rect = self.image.get_rect(center = self.mario.rect.center)
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100  
            self.duration = 1000
            self.animation_done = False
            self.start_time = pygame.time.get_ticks()
        
        def update(self):
            self.rect.center = self.mario.rect.center
            
            if pygame.time.get_ticks() - self.last_update > self.frame_rate:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]

            if pygame.time.get_ticks() - self.start_time > self.duration:  # 持续一段时间后自动删除
                self.kill()


    class AnimatedArrowLuna(pygame.sprite.Sprite):
        def __init__(self, x, y, frames):
            super().__init__() 
            self.frames = frames
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 5
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100  

        def update(self):
            # 当他正在动
            self.rect.x += self.speed
            if self.rect.left > WIDTH:
                self.kill()

            # 动画
            if pygame.time.get_ticks() - self.last_update > self.frame_rate:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]



    class AnimatedArrowHawk(pygame.sprite.Sprite):
        def __init__(self, x, y, frames):
            super().__init__() 
            self.frames = frames
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 5
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100  

        def update(self):
            # 当他正在动
            self.rect.x += self.speed
            if self.rect.left > WIDTH:
                self.kill()

            # 动画
            if pygame.time.get_ticks() - self.last_update > self.frame_rate:
                self.last_update = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]

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
    game_over = False
    start_time = pygame.time.get_ticks()  # Get initial time in milliseconds
    time_limit = 121000


    # Game loop
    running = True
    while running:
        clock.tick(60)
        screen.blit(background_img, (0, 0))

        current_time = pygame.time.get_ticks()  # Get current time
        elapsed_time = current_time - start_time  # Time passed since start
        remaining_time = max(0, time_limit - elapsed_time)  # Prevent negative time
        minutes = remaining_time // 60000
        seconds = remaining_time % 60000 // 1000

        timer_color = RED if remaining_time <= 10000 else WHITE
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, timer_color)
        screen.blit(timer_text, (WIDTH // 2 - 50, 120))

        if remaining_time <= 0 and not game_over:
            game_over = True
            time_up_text = font.render("TIME'S UP! GAME OVER.", True, RED)
            screen.blit(time_up_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)  # Show message for 3 seconds
            running = False


        x = 290
        y = 0
        box = pygame.Surface((620, 120), pygame.SRCALPHA)
        box.fill((0, 0, 0, 0))  # Fully transparent base
        pygame.draw.rect(box, (*BLACK, 100), box.get_rect(), border_radius=12)
        screen.blit(box, (x, y))

        x_box = 300
        y_box = 15
        weapon_buttons.clear()
        for weapon_name, img in original_weapon_images.items():      # loop thought the weapon image
            scaled_images = pygame.transform.smoothscale(img, (90, 90))
            img_rect = pygame.Rect(x_box, y_box, 90, 90)
            screen.blit(scaled_images, (x_box, y_box))
            weapon_buttons.append((weapon_name, img_rect)) 
            x_box += 100      # Spacing between images

        
        # Mario 的命
        mario_bar_width = 250
        mario_bar_height = 15
        mario_health_ratio = mario.health / 100
        pygame.draw.rect(screen, GREY, (20, 50, mario_bar_width, mario_bar_height), border_radius=5)  # Background
        pygame.draw.rect(screen, GREEN, (20, 50, mario_bar_width * mario_health_ratio, mario_bar_height), border_radius=5)  # Fill
        mario_text = font.render(f"Mario HP: {mario.health}/100", True, WHITE)
        screen.blit(mario_text, (20, 20))


        # Boss 的命
        boss_bar_width = 250
        boss_bar_height = 15
        boss_health_ratio = boss.health / 10000
        pygame.draw.rect(screen, GREY, (930, 50, boss_bar_width, boss_bar_height), border_radius=5)  # Background
        pygame.draw.rect(screen, RED, (930, 50, boss_bar_width * boss_health_ratio, boss_bar_height), border_radius=5)  # Fill
        boss_text = font.render(f"Boss HP: {boss.health}/10000", True, WHITE)
        screen.blit(boss_text, (930, 20))

    
        

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

                        if weapon_name == "Essence of Renewal":
                            effect = AnimatedAddHealth(mario, add_health_frames)
                            all_sprites.add(effect)
                            add_health_sound.play()

                        if weapon_name == "Essence of Renewal":
                            effect = AnimatedAddHealth(mario, add_health_frames)
                            all_sprites.add(effect)
                            add_health_sound.play()


        if not game_over:        
            all_sprites.update()
            for bullet in bullets:
                hit_fireballs = pygame.sprite.spritecollide(bullet, fireballs, False)
                for fireball in hit_fireballs:
                    bullet.kill()  # Remove bullet on hit
                    fireball.hit_count += 1  
                    if fireball.hit_count >= 2:
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
                    mario.activate_message = "Blocked by Aegis Shield!"
                    mario.activate_message_timer = pygame.time.get_ticks() + 2000
                    continue  # 没伤害
                mario.health -= random.randint(5, 8)
                if mario.health <= 0:
                    mario.lives -= 1
                    running = False
            
    
        
        all_sprites.draw(screen)
        mario.draw_shield(screen) 
    

        # Activated message
        if mario.activate_message and pygame.time.get_ticks() < mario.activate_message_timer:
            msg = font.render(mario.activate_message, True, RED)
            msg_x = WIDTH // 2 - msg.get_width() // 2
            msg_y = HEIGHT - 60
            

            msg_bg = pygame.Surface((msg.get_width() + 20, msg.get_height() + 10)) # Background box
            msg_bg.set_alpha(100)  # Transparency
            msg_bg.fill(GREY)
            screen.blit(msg_bg, (msg_x - 10, msg_y - 5))  # Draw background
            screen.blit(msg, (msg_x, msg_y))         # Draw message


        # Show expired weapon message
        if mario.expired_message and pygame.time.get_ticks() < mario.expired_message_timer:
            msg = font.render(mario.expired_message, True, RED)
            msg_x = WIDTH // 2 - msg.get_width() // 2
            msg_y = HEIGHT - 30

            msg_bg = pygame.Surface((msg.get_width() + 20, msg.get_height() + 10)) # Background box
            msg_bg.set_alpha(100)  # Transparency
            msg_bg.fill(GREY)
            screen.blit(msg_bg, (msg_x - 10, msg_y - 5))  # Draw background
            screen.blit(msg, (msg_x, msg_y))         # Draw message

        pygame.display.flip()

    return True

# Main game loop
running = True
while running:
    clock.tick(60)
    
    if current_state == MENU:
        screen.fill(WHITE)
        start_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if start_button.is_clicked(event):
                current_state = BOSS_STAGE
                click_sound.play()
                # Run the boss stage and check if we should return to menu or quit
                should_continue = boss_stage()
                if not should_continue:
                    running = False
                else:
                    current_state = MENU  # Return to menu after boss stage ends
    
    pygame.display.update()

pygame.quit()
sys.exit()
