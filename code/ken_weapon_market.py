import pygame
import sys

WIDTH, HEIGHT = 1000, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD =  (255, 215, 0)
PURPLE = (150, 0, 150)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weapon Market")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 20)

player_coins = 1500
player_gems = 500

market_item = [
    {"name": "Golden Sword", "price": 1000, "currency": "coins"},
    {"name": "Golden Sword", "price": 1000, "currency": "gems"},
    {"name": "Golden Sword", "price": 1000, "currency": "coins"},
    {"name": "Golden Sword", "price": 1000, "currency": "gems"},
    {"name": "Golden Sword", "price": 1000, "currency": "coins"},
    {"name": "Golden Sword", "price": 1000, "currency": "gems"},
]

running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    coins_text = font.render(f"Coins : {player_coins}", True, (GOLD))
    gems_text = font.render(f"Gems : {player_gems}", True, (PURPLE))
    screen.blit(coins_text, (30, 20))
    screen.blit(gems_text, (30 + coins_text.get_width() + 20, 20))

    for i, item in enumerate(market_item):
        col = 3
        x = 100 + (i % col) * 250
        y = 100 + (i // col) * 250
        box = pygame.Rect(x, y, 200, 150)
        pygame.draw.rect(screen, (180, 180, 180), box)
        
        name_text = font.render(item["name"], True, (BLACK))
        screen.blit(name_text, (x + box.width // 2 - name_text.get_width() // 2, y + 155))
        
        color = (GOLD) if item["currency"] == "coins" else (PURPLE)
        price_text = font.render(f"{item['price']} {item['currency']}", True, color)
        screen.blit(price_text, (x + box.width // 2 - price_text.get_width() // 2, y + 180))



    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit