import pygame
import sys

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weapon Market")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 20)

player_coins = 1500
player_gems = 500

market_item = {
    "name": "Golden Sword", "price": 1000, "currency": "coins"
}

running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    coins_text = font.render(f"Coins : {player_coins}", True, (0, 255, 0))
    gems_text = font.render(f"Gems : {player_gems}", True, (150, 0, 150))
    screen.blit(coins_text, (30, 20))
    screen.blit(gems_text, (30, 60))

    item_x = 100
    item_y = 100
    item_box = pygame.Rect(item_x, item_y, 200, 150)
    pygame.draw.rect(screen, (180, 180, 180), item_box)

   

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit