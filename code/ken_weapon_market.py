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
LIGHT_GREEN = (0, 255, 0)
GREY = (200, 200, 200)
BLUE = (135, 206, 235)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weapon Market")
clock = pygame.time.Clock()

coin_icon = pygame.image.load(os.path.join("assets", "images", "dollar.png")).convert_alpha()
coin_icon = pygame.transform.scale(coin_icon, (25, 25))
gem_icon = pygame.image.load(os.path.join("assets", "images", "gem.png")).convert_alpha()
gem_icon = pygame.transform.scale(gem_icon, (25, 25))
girl_image = pygame.image.load(os.path.join("assets", "images", "girl.png")).convert_alpha()
girl_image = pygame.transform.scale(girl_image, (450, 700))
arrow_image = pygame.image.load(os.path.join("assets", "images", "arrow.png")).convert_alpha()
arrow_image = pygame.transform.scale(arrow_image, (50, 60))

weapon_images = {
    "Lion Sword": pygame.image.load(os.path.join("assets", "images", "Lion_sword.png")).convert_alpha(),
    #"Hawk's Eye": pygame.image.load(os.path.join("assets", "images", "hawks_eye.png")).convert_alpha(),
    "Luna Bow": pygame.image.load(os.path.join("assets", "images", "Luna_bow.png")).convert_alpha(),
    "Phoenix Feather": pygame.image.load(os.path.join("assets", "images", "Phoenix_feather.png")).convert_alpha(),
    #"Hydro Strike": pygame.image.load(os.path.join("assets", "images", "hydro_strike.png")).convert_alpha(),
    #"Libra of Eternity": pygame.image.load(os.path.join("assets", "images", "libra_eternity.png")).convert_alpha(),
    #"Aegis Shield": pygame.image.load(os.path.join("assets", "images", "aegis_shield.png")).convert_alpha(),
    #"Thunder Axe": pygame.image.load(os.path.join("assets", "images", "thunder_axe.png")).convert_alpha(),
    #"Essence of Renewal": pygame.image.load(os.path.join("assets", "images", "essence_renewal.png")).convert_alpha()
}

for key in weapon_images:
    weapon_images[key] = pygame.transform.scale(weapon_images[key], (90, 90))

click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click.wav"))

font = pygame.font.SysFont("arial", 20)

player_coins = 1500
player_gems = 500

buy_buttons = []
inventory = []
message = ""
message_timer = 0

market_item = [
    {"name": "Lion Sword", "price": 100, "currency": "coins", "bought": False},
    {"name": "Hawk's Eye", "price": 100, "currency": "coins", "bought": False},
    {"name": "Luna Bow", "price": 100, "currency": "gems", "bought": False},
    {"name": "Phoenix Feather", "price": 100, "currency": "gems", "bought": False},
    {"name": "Hydro Strike", "price": 100, "currency": "coins", "bought": False},
    {"name": "Libra of Eternity", "price": 100, "currency": "gems", "bought": False},
    {"name": "Aegis Shield", "price": 100, "currency": "coins", "bought": False},
    {"name": "Thunder Axe", "price": 100, "currency": "gems", "bought": False},
    {"name": "Essence of Renewal", "price": 100, "currency": "coins", "bought": False},
]


def draw_stat_box(surface, x, y, width, height, color, alpha):
    s = pygame.Surface((width, height), pygame.SRCALPHA)  # Transparent surface
    pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=12)  # Rounded rectangle
    surface.blit(s, (x, y))  # Draw it on your screen

arrow_rect = arrow_image.get_rect(topleft=(10, 5))  # Set position

def draw_arrow(surface, arrow_image, arrow_rect):
    mx, my = pygame.mouse.get_pos()
    if arrow_rect.collidepoint(mx, my):
        actual_arrow = arrow_image.copy()
        actual_arrow.fill((255, 255, 255, 50), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(actual_arrow, arrow_rect)
    else:
        screen.blit(arrow_image, arrow_rect)

running = True
while running:
    clock.tick(FPS)
    screen.fill(BROWN)
    buy_buttons = []
    
    draw_arrow(screen, arrow_image, arrow_rect)  # Draw the arrow

    title_text = font.render("Weapon Market", True, WHITE)
    screen.blit(title_text, (70, 20))

    draw_stat_box(screen, 230, 15, 225, 35, GREY, 150)  # Background
    
    screen.blit(coin_icon, (250, 20))
    coins_text = font.render(f"{player_coins}", True, WHITE)
    screen.blit(coins_text, (280, 20))
    
    screen.blit(gem_icon, (300 + coins_text.get_width() + 30, 20))
    gems_text = font.render(f"{player_gems}", True, WHITE)
    screen.blit(gems_text, (300 + coins_text.get_width() + 60, 20))

    for i, item in enumerate(market_item):
        col = 3
        x = 230 + (i % col) * 230
        y = 80 + (i // col) * 250
        box = pygame.Rect(x, y, 200, 130)
        pygame.draw.rect(screen, GREY, box)

        if item["name"] in weapon_images:  #武器照片
           img = weapon_images[item["name"]]
           img_x = x + box.width // 2 - img.get_width() // 2
           img_y = y + 10  
           screen.blit(img, (img_x, img_y))
        
        name_text = font.render(item["name"], True, (BLACK))  #Name text
        screen.blit(name_text, (x + box.width // 2 - name_text.get_width() // 2, y + 135))
        
        price_text = font.render(str(item['price']) , True, WHITE)  #Price text

        if item["currency"] == "coins":
            icon = coin_icon   
        else:
            icon = gem_icon   
            
        icon_width = icon.get_width()
        text_width = price_text.get_width()
        total_width = icon_width + 5 + text_width  #icon + space + text

        center_iconprice_x = x + box.width // 2 - total_width // 2   #Center the whole thing
        iconprice_y = y + 160

        screen.blit(icon, (center_iconprice_x, iconprice_y))
        screen.blit(price_text, (center_iconprice_x + icon_width + 5, iconprice_y))

        if not item["bought"]:
            buy_button = pygame.Rect(x + 35, y + 100, 130, 25) #Buy button box
            hover_color = LIGHT_GREEN
            normal_color = GREEN
            if buy_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, hover_color, buy_button, border_radius=12)
            else :
                pygame.draw.rect(screen, normal_color, buy_button ,border_radius=12)

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
            if arrow_rect.collidepoint(mx, my):
                running = False 


            for i, button in enumerate(buy_buttons):
                if button and button.collidepoint(mx, my):  # All logic stays inside this block
                    click_sound.play()
                    item = market_item[i]
                    currency = item["currency"]
                    price = item["price"]

                    if currency == "coins" and player_coins >= price:
                        player_coins -= price
                        item["bought"] = True
                        inventory.append(item["name"])
                        click_sound.play()
                        message = f"Bought {item['name']} for {price} coins!"
                        message_timer = pygame.time.get_ticks() + 2000
                    elif currency == "gems" and player_gems >= price:
                        player_gems -= price
                        item["bought"] = True
                        inventory.append(item["name"])
                        click_sound.play()
                        message = f"Bought {item['name']} for {price} gems!"
                        message_timer = pygame.time.get_ticks() + 2000
                    else:
                        message = "Not enough resources!"
                        message_timer = pygame.time.get_ticks() + 2000

    if message and pygame.time.get_ticks() < message_timer:
        msg_text = font.render(message, True, RED)
        msg_x = WIDTH // 2 - msg_text.get_width() // 2
        msg_y = HEIGHT - 30

       
        msg_bg = pygame.Surface((msg_text.get_width() + 20, msg_text.get_height() + 10)) # Background box
        msg_bg.set_alpha(100)  # Transparency
        msg_bg.fill(GREY)
        screen.blit(msg_bg, (msg_x - 10, msg_y - 5))  # Draw background
        screen.blit(msg_text, (msg_x, msg_y))         # Draw message

    inventory_box = pygame.Rect(10, 100, 200, 35)  # Inventory background box
    pygame.draw.rect(screen, BLACK, inventory_box ,border_radius=12)

    inventory_title_text = font.render("Inventory:", True, WHITE)
    screen.blit(inventory_title_text, (20, 105))

    for i, item_name in enumerate(inventory):
        item_text = font.render(item_name, True, BLACK)
        screen.blit(item_text, (30, 135 + i * 25))


    
    screen.blit(girl_image, (WIDTH - 340, HEIGHT - 700))

    pygame.display.update()
    
pygame.quit()
sys.exit