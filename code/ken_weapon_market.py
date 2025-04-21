import pygame
import sys

WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE =  (255, 215, 0)
GOLD = (150, 0, 150)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weapon Market")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 20)

player_coins = 1500
player_gems = 500

market_item = {
    "name": "Golden Sword", "price": 1000, "currency": "gems"
}

running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    coins_text = font.render(f"Coins : {player_coins}", True, (GOLD))
    gems_text = font.render(f"Gems : {player_gems}", True, (PURPLE))
    screen.blit(coins_text, (30, 20))
    screen.blit(gems_text, (30, 50))

    item_x = 100
    item_y = 100
    item_box = pygame.Rect(item_x, item_y, 200, 150)
    pygame.draw.rect(screen, (180, 180, 180), item_box)

    name_text = font.render(market_item["name"], True, (BLACK))
    screen.blit(name_text, (item_x + item_box.width // 2 - name_text.get_width() // 2, item_y + 155))

    color = (PURPLE) if market_item["currency"] == "coins" else (GOLD)
    price_text = font.render(f"{market_item['price']} {market_item['currency']}", True, color)
    screen.blit(price_text, (item_x + item_box.width // 2 - price_text.get_width() // 2, item_y + 180))



    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit