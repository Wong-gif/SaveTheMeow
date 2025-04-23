import pygame
import sys
import os

WIDTH, HEIGHT = 1200, 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD =  (255, 215, 0)
PURPLE = (150, 0, 150)
GREEN = (0, 200, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weapon Market")
clock = pygame.time.Clock()

click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click.wav"))

font = pygame.font.SysFont("arial", 20)

player_coins = 1500
player_gems = 500

buy_buttons = []
message = ""
message_timer = 0

market_item = [
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "gems", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "gems", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "gems", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Golden Sword", "price": 100, "currency": "coins", "bought": False},
]

running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    buy_buttons = []

    coins_text = font.render(f"Coins : {player_coins}", True, (GOLD))
    gems_text = font.render(f"Gems : {player_gems}", True, (PURPLE))
    screen.blit(coins_text, (30, 20))
    screen.blit(gems_text, (30 + coins_text.get_width() + 20, 20))

    for i, item in enumerate(market_item):
        col = 4
        x = 50 + (i % col) * 220
        y = 80 + (i // col) * 250
        box = pygame.Rect(x, y, 190, 130)
        pygame.draw.rect(screen, (180, 180, 180), box)
        
        name_text = font.render(item["name"], True, (BLACK))
        screen.blit(name_text, (x + box.width // 2 - name_text.get_width() // 2, y + 135))
        
        color = (GOLD) if item["currency"] == "coins" else (PURPLE)
        price_text = font.render(f"{item['price']} {item['currency']}", True, color)
        screen.blit(price_text, (x + box.width // 2 - price_text.get_width() // 2, y + 160))
        
        if not item["bought"]:
            buy_button = pygame.Rect(x + 35, y + 100, 120, 25) #Buy button box
            pygame.draw.rect(screen, GREEN, buy_button)
            
            buy_text = font.render("Buy", True, WHITE) #Buy text
            text_x = buy_button.x + buy_button.width // 2 - buy_text.get_width() // 2
            text_y = buy_button.y + buy_button.height // 2 - buy_text.get_height() // 2
            screen.blit(buy_text, (text_x, text_y))
            buy_buttons.append(buy_button)
        else :
            sold_out_text = font.render("Sold out", True, WHITE) #Sold out text
            text_x = box.x + box.width // 2 - sold_out_text.get_width() // 2
            text_y = box.y + box.height // 2 - sold_out_text.get_height() // 2
            screen.blit(sold_out_text, (text_x, text_y))
            buy_buttons.append(None)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for i, button in enumerate(buy_buttons):
                if button and button.collidepoint(mx, my):  # All logic stays inside this block
                    click_sound.play()
                    item = market_item[i]
                    currency = item["currency"]
                    price = item["price"]

                    if currency == "coins" and player_coins >= price:
                        player_coins -= price
                        item["bought"] = True
                        click_sound.play()
                        message = f"Bought {item['name']} for {price} coins!"
                        message_timer = pygame.time.get_ticks() + 2000
                    elif currency == "gems" and player_gems >= price:
                        player_gems -= price
                        item["bought"] = True
                        click_sound.play()
                        message = f"Bought {item['name']} for {price} gems!"
                        message_timer = pygame.time.get_ticks() + 2000
                    else:
                        message = "Not enough resources!"
                        message_timer = pygame.time.get_ticks() + 2000
    
    
    pygame.display.update()
    if message and pygame.time.get_ticks() < message_timer:
        msg_text = font.render(message, True, (255, 0, 0))
        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT - 40))


pygame.quit()
sys.exit