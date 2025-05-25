def open_store(username):
    import pygame
    import sys
    import os
    import json 

    WIDTH, HEIGHT = 1200, 800
    FPS = 60
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 200, 0)
    LIGHT_GREEN = (0, 255, 100)
    GREY = (200, 200, 200)
    LIGHT_GREY = (220, 220, 220)


    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Weapon Market")
    clock = pygame.time.Clock()

    #background
    background = pygame.image.load(os.path.join("assets", "images", "weapon_background.jpg")).convert_alpha()
    # coin icon
    coin_icon = pygame.image.load(os.path.join("assets", "images", "dollar.png")).convert_alpha()
    coin_icon = pygame.transform.scale(coin_icon, (25, 25))
    # gem icon
    gem_icon = pygame.image.load(os.path.join("assets", "images", "gem.png")).convert_alpha()
    gem_icon = pygame.transform.scale(gem_icon, (25, 25))
    #girl image
    girl_image = pygame.image.load(os.path.join("assets", "images", "girl.png")).convert_alpha()
    girl_image = pygame.transform.scale(girl_image, (450, 700))
    # Go out arrow
    arrow_image = pygame.image.load(os.path.join("assets", "images", "arrow.png")).convert_alpha()
    arrow_image = pygame.transform.scale(arrow_image, (50, 60))

    # Sound & Music
    click_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "click.wav"))
    buying_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "buy_sound.wav"))
    pygame.mixer.music.load(os.path.join("assets", "sounds", "weaponback_music.wav"))
    pygame.mixer.music.set_volume(0.5)  # Adjust volume


    font = pygame.font.SysFont("arial", 20)

    original_weapon_images = {
        "Phoenix Feather": pygame.image.load(os.path.join("assets", "images", "Phoenix_feather.png")).convert_alpha(),
        "Essence of Renewal": pygame.image.load(os.path.join("assets", "images", "Essence_renewal.png")).convert_alpha(),
        "Luna Bow": pygame.image.load(os.path.join("assets", "images", "Luna_bow.png")).convert_alpha(),
        "Hydro Strike": pygame.image.load(os.path.join("assets", "images", "Hydro_strike.png")).convert_alpha(),
        "Aegis Shield": pygame.image.load(os.path.join("assets", "images", "Aegis_shield.png")).convert_alpha(),
        "Hawk's Eye": pygame.image.load(os.path.join("assets", "images", "Hawk_eye.png")).convert_alpha(),
        "Lion Sword": pygame.image.load(os.path.join("assets", "images", "Lion_sword.png")).convert_alpha(),
        "Shadow Saber": pygame.image.load(os.path.join("assets", "images", "Shadow_saber.png")).convert_alpha(),
        "Thunder Axe": pygame.image.load(os.path.join("assets", "images", "Thunder_axe.png")).convert_alpha()
    }

    weapon_images = {
        name: pygame.transform.smoothscale(img, (150, 150))
        for name, img in original_weapon_images.items()
    }

    weapon_description = {
        "Phoenix Feather": {"description": "Each arrow has 120 damage. Only for 10 seconds."},
        "Essence of Renewal": {"description": "Restore 50 health points for three times."},
        "Luna Bow": {"description": "Each arrow has 150 damage. Only for 10 seconds."},
        "Hydro Strike": {"description": "Each bullet has 200 points of attack. Only for 10 seconds"},
        "Aegis Shield": {"description": "30% probability to block attack."},
        "Hawk's Eye": {"description": "Each arrow has 130 damage. Only for 10 seconds."},
        "Lion Sword": {"description": "Each swing of the sword has 150 points of attack. Only 5 chances."},
        "Shadow Saber": {"description": "30% probability to block attack."}, 
        "Thunder Axe": {"description": "30% probability to stun the enemy for 3 seconds within 20 seconds."}
    }
        

    filename = f"{username}.txt"

    # 尝试从 jh.txt 中加载数据
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    
        total_coins = data["game1"]["Best Coins"] + data["game2"]["Best Coins"]
        total_diamonds = data["game1"]["Best Diamonds"] + data["game2"]["Best Diamonds"]
        
        player_coins = total_coins
        player_gems = total_diamonds
        
    except FileNotFoundError:
        print("警告：jh.txt 未找到，使用默认值")
        player_coins = 700
        player_gems = 500
    except KeyError:
        print("警告：jh.txt 格式错误或缺少必要字段，使用默认值")
        player_coins = 700
        player_gems = 500
    except json.JSONDecodeError:
        print("警告：jh.txt 不是有效的 JSON，使用默认值")
        player_coins = 700
        player_gems = 500

    market_item = [
        {"name": "Phoenix Feather", "price": 160, "currency": "coins", "bought": False},
        {"name": "Essence of Renewal", "price": 130, "currency": "coins", "bought": False},
        {"name": "Luna Bow", "price": 228, "currency": "coins", "bought": False},
        {"name": "Hydro Strike", "price": 108, "currency": "gems", "bought": False},
        {"name": "Aegis Shield", "price": 45, "currency": "gems", "bought": False},
        {"name": "Hawk's Eye", "price": 65, "currency": "gems", "bought": False},
        {"name": "Lion Sword", "price": 100, "currency": "coins", "bought": False},
        {"name": "Shadow Saber", "price": 100, "currency": "coins", "bought": False},
        {"name": "Thunder Axe", "price": 150, "currency": "coins", "bought": False}
    ]

    # Gems and coins that on top
    def draw_stat_box(surface, x, y, width, height, color, alpha):
        s = pygame.Surface((width, height), pygame.SRCALPHA)  # Transparent surface
        pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=12)  # Rounded rectangle
        surface.blit(s, (x, y))  # Draw it on your screen

    # Arrow (hover or actual)
    def draw_arrow(surface, arrow_image, arrow_rect):
        mx, my = pygame.mouse.get_pos()
        if arrow_rect.collidepoint(mx, my):
            actual_arrow = arrow_image.copy()
            actual_arrow.fill((255, 255, 255, 50), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(actual_arrow, arrow_rect)
        else:
            screen.blit(arrow_image, arrow_rect) # make the image follow the rect


    arrow_rect = pygame.Rect(10, 5, 50, 60)  # Set position
    selected_item = None  # 选中的物品
    show_item_details = False  # 是否显示详情窗口
    inventory_boss = []
    inventory_farm = []
    message = ""
    message_timer = 0
    pygame.mixer.music.play(-1)

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        # Save inventory back to the user's file
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            # 自动补全缺失的 inventory 字段
            if "inventory" not in data:
                data["inventory"] = {
                    "Weapon for Boss": [],
                    "Weapon for Farm": []
                }
        except FileNotFoundError:
            data = {
                "game1": {"Coins": 0, "Diamonds": 0, "Best Coins": 0, "Best Diamonds": 0},
                "game2": {"Coins": 0, "Diamonds": 0, "Best Coins": 0, "Best Diamonds": 0},
                "inventory": {"Weapon for Boss": [], "Weapon for Farm": []}
            }

        # 更新 inventory 数据
        data["inventory"]["Weapon for Boss"] = inventory_boss
        data["inventory"]["Weapon for Farm"] = inventory_farm

        # 写回文件
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Inventory saved for {username}")
        
        draw_arrow(screen, arrow_image, arrow_rect)  # Draw the arrow

        title_text = font.render("Weapon Market", True, BLACK) # Draw weapon market text
        screen.blit(title_text, (70, 20))

        draw_stat_box(screen, 250, 15, 225, 35, GREY, 100)  # Background
        
        screen.blit(coin_icon, (270, 20))  # Draw coin icon
        coins_text = font.render(f"{player_coins}", True, WHITE)
        screen.blit(coins_text, (305, 20))
        
        screen.blit(gem_icon, (320 + coins_text.get_width() + 30, 20))   # Draw gem icon
        gems_text = font.render(f"{player_gems}", True, WHITE)
        screen.blit(gems_text, (325 + coins_text.get_width() + 60, 20))
        
        # Inventory background box（boss)
        inventory_box_width = 215
        inventory_box_height = max(150, 40 + len(inventory_boss) * 40 + 20)
        inventory_box = pygame.Surface((inventory_box_width, inventory_box_height), pygame.SRCALPHA)
        pygame.draw.rect(inventory_box, (*BLACK, 100), inventory_box.get_rect() ,border_radius=12)
        screen.blit(inventory_box, (10, 90))

        #Inventory title
        inventory_title_text = font.render("Inventory for boss :", True, WHITE)
        screen.blit(inventory_title_text, (20, 105))

        for i, item_name in enumerate(inventory_boss):  # Only show first 6 items
            if item_name in weapon_images:
                img = pygame.transform.scale(weapon_images[item_name], (30, 30))
                screen.blit(img, (20, 150 + i * 40))
                name_text = font.render(item_name, True, WHITE)
                screen.blit(name_text, (60, 155 + i * 40))

        # Inventory background box （Bottom)
        inventory_box_width = 215
        inventory_box_height = max(150, 40 + len(inventory_farm) * 40 + 20)
        inventory_box = pygame.Surface((inventory_box_width, inventory_box_height), pygame.SRCALPHA)
        pygame.draw.rect(inventory_box, (*BLACK, 100), inventory_box.get_rect() ,border_radius=12)
        screen.blit(inventory_box, (10, 550))

        #Inventory title
        inventory_title_text = font.render("Inventory for farm :", True, WHITE)
        screen.blit(inventory_title_text, (20, 565))


        for i, item_name in enumerate(inventory_farm):
            if item_name in weapon_images:
                img = pygame.transform.scale(weapon_images[item_name], (30, 30))  # Small icon
                screen.blit(img, (20, 610 + i * 40))  # Draw image
                name_text = font.render(item_name, True, WHITE)
                screen.blit(name_text, (60, 615 + i * 40))  # Name next to image

        screen.blit(girl_image, (WIDTH - 340, HEIGHT - 700))

        for i, item in enumerate(market_item):    # 9 Boxes 
            col = 3
            x = 240 + (i % col) * 230
            y = 80 + (i // col) * 230
            box = pygame.Surface((190, 160), pygame.SRCALPHA)
            box.fill((0, 0, 0, 0))  # Fully transparent base
            pygame.draw.rect(box, (*GREY, 100), box.get_rect(), border_radius=12)
            screen.blit(box, (x, y))


            if item["name"] in weapon_images:  # Weapon image
                img = weapon_images[item["name"]]
                img_x = x + box.get_width() // 2 - img.get_width() // 2
                img_y = y + 5  
                screen.blit(img, (img_x, img_y))
            
            name_text = font.render(item["name"], True, (WHITE))  #Name text
            screen.blit(name_text, (x + box.get_width() // 2 - name_text.get_width() // 2, y + 163))
            
            price_text = font.render(str(item['price']) , True, WHITE)  #Price text

            if item["currency"] == "coins":
                icon = coin_icon   
            else:
                icon = gem_icon   
                
            icon_width = icon.get_width()
            text_width = price_text.get_width()
            total_width = icon_width + 5 + text_width  #icon + space + text

            center_iconprice_x = x + box.get_width() // 2 - total_width // 2   #Center the whole thing
            iconprice_y = y + 190

            screen.blit(icon, (center_iconprice_x, iconprice_y))
            screen.blit(price_text, (center_iconprice_x + icon_width + 5, iconprice_y))

            if item["bought"]:
                sold_out_text = font.render("Sold out", True, RED)
                text_x = x + box.get_width() // 2 - sold_out_text.get_width() // 2
                text_y = y + box.get_height() // 2 - sold_out_text.get_height() // 2
                screen.blit(sold_out_text, (text_x, text_y))

        for event in pygame.event.get():      # Mouse click
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if arrow_rect.collidepoint(mx, my):
                    click_sound.play()
                    for alpha in range(0, 300, 15):    # Fade out function
                        fade = pygame.Surface((WIDTH, HEIGHT))
                        fade.fill((0, 0, 0))
                        fade.set_alpha(alpha)
                        screen.blit(fade, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(30)
                    running = False

                
                elif show_item_details and selected_item:    
                    if cancel_button.collidepoint(mx, my):
                        click_sound.play()
                        show_item_details = False
                    elif buy_button.collidepoint(mx, my): 
                        item = selected_item
                        currency = item["currency"]
                        price = item["price"]

                        if currency == "coins" and player_coins >= price:
                            player_coins -= price
                            item["bought"] = True
                            if item["name"] in ["Phoenix Feather", "Essence of Renewal", "Luna Bow", 
                            "Hydro Strike", "Aegis Shield", "Hawk's Eye"]:
                                inventory_boss.append(item["name"])  # 前6个进上面
                            else:
                                inventory_farm.append(item["name"])  # 后3个进下面
                            buying_sound.play()
                            message = f"Bought {item['name']} for {price} coins!"
                            show_item_details = False
                            message_timer = pygame.time.get_ticks() + 2000
                        elif currency == "gems" and player_gems >= price:
                            player_gems -= price
                            item["bought"] = True
                            if item["name"] in ["Phoenix Feather", "Essence of Renewal", "Luna Bow", 
                            "Hydro Strike", "Aegis Shield", "Hawk's Eye"]:
                                inventory_boss.append(item["name"])  # 前6个进上面
                            else:
                                inventory_farm.append(item["name"])  # 后3个进下面
                            buying_sound.play()
                            message = f"Bought {item['name']} for {price} gems!"
                            show_item_details = False
                            message_timer = pygame.time.get_ticks() + 2000
                        else:
                            message = "Not enough resources!"
                            message_timer = pygame.time.get_ticks() + 2000
                            show_item_details = False

                else:
                    for i, item in enumerate(market_item):
                        col = 3
                        x = 230 + (i % col) * 230
                        y = 80 + (i // col) * 230
                        box = pygame.Rect(x, y, 200, 160)
                        if box.collidepoint(mx, my) and not item["bought"]:  # Only if the mouse clicked the box and the item is NOT bought yet
                            click_sound.play()
                            selected_item = item
                            show_item_details = True
                            break



        if message and pygame.time.get_ticks() < message_timer:    # Message that show below   
            msg_text = font.render(message, True, RED)
            msg_x = WIDTH // 2 - msg_text.get_width() // 2
            msg_y = HEIGHT - 30

        
            msg_bg = pygame.Surface((msg_text.get_width() + 20, msg_text.get_height() + 10)) # Background box
            msg_bg.set_alpha(100)  # Transparency
            msg_bg.fill(GREY)
            screen.blit(msg_bg, (msg_x - 10, msg_y - 5))  # Draw background
            screen.blit(msg_text, (msg_x, msg_y))         # Draw message



    

        # 弹出物品详情窗口
        if show_item_details and selected_item:
        # 半透明遮罩
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            popup_width, popup_height = 600, 400
            popup_x = WIDTH // 2 - popup_width // 2
            popup_y = HEIGHT // 2 - popup_height // 2
            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
            pygame.draw.rect(screen, WHITE, popup_rect, border_radius=15)

            # 标题
            title_font = pygame.font.SysFont("arial", 30)
            title_text = title_font.render(selected_item["name"], True, BLACK)
            screen.blit(title_text, (popup_x + popup_width // 2 - title_text.get_width() // 2, popup_y + 15))

            # 武器图片
            img = original_weapon_images.get(selected_item["name"])
            if img:
                img = pygame.transform.smoothscale(img, (190, 190))
                screen.blit(img, (popup_x + popup_width // 2 - img.get_width() // 2, popup_y + 70))

            # 描述
            desc_font = pygame.font.SysFont("arial", 22)
            description = weapon_description[selected_item["name"]]["description"]
            desc_text = desc_font.render(description, True, BLACK)
            desc_x = popup_x + popup_width // 2 - desc_text.get_width() // 2
            desc_y = popup_y + popup_height // 2 - desc_text.get_height() // 2 + 90 
            screen.blit(desc_text, (desc_x, desc_y))

            # 按钮
            cancel_button = pygame.Rect(popup_x + 50, popup_y + popup_height - 60, 100, 40)
            buy_button = pygame.Rect(popup_x + popup_width - 150, popup_y + popup_height - 60, 100, 40)
            
            mx, my = pygame.mouse.get_pos()
            cancel_hovered = cancel_button.collidepoint(mx, my)
            buy_hovered = buy_button.collidepoint(mx, my)
            
            cancel_color = LIGHT_GREY if cancel_hovered else GREY
            pygame.draw.rect(screen, cancel_color, cancel_button, border_radius=8)
        
            buy_color = LIGHT_GREEN if buy_hovered else GREEN
            pygame.draw.rect(screen, buy_color, buy_button, border_radius=8)

            cancel_text = font.render("Cancel", True, BLACK)
            buy_text = font.render("Buy", True, BLACK)
            screen.blit(cancel_text, (cancel_button.x + cancel_button.width//2 - cancel_text.get_width()//2, cancel_button.y + 8))
            screen.blit(buy_text, (buy_button.x + buy_button.width//2 - buy_text.get_width()//2, buy_button.y + 8))

        
        pygame.display.update()
        
    return