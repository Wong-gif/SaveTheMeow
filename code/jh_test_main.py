def platform_map():
    import pygame
    import sys
    from jh_game1 import Game1
    from jh_game2 import Game2
    from jh_game_summary import GameSummary

    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800 
    FPS = 60
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 200, 0)

    MENU = "menu"
    GAME1 = "game1"
    GAME2 = "game2"
    SUMMARY = "summary"

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Save The Meow")
    clock = pygame.time.Clock()

    background = pygame.image.load('assets/images/background.png').convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  

    game1 = Game1(screen)
    game2 = Game2(screen)

    final_score = game2.score  # 游戏的最终分数
    diamond_score = game2.diamonds_collected  # 玩家收集的钻石数量


    levels_data = {
        "level1": {"score": game1.score, "time_ms": game1.time_left, "coins": game1.coins_collected, "diamonds": game1.diamonds_collected},
        "level2": {"score": game2.score, "time_ms": game2.time_left, "coins": game2.coins_collected, "diamonds": game2.diamonds_collected}
    }

    summary = GameSummary(screen, levels_data, game1.coins_collected, game2.coins_collected, game1.diamonds_collected, game2.diamonds_collected)

    current_state = MENU

    class Button:
        def __init__(self, x, y, width, height, text):
            self.rect = pygame.Rect(x, y, width, height)#position
            self.text = text
            self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)
            self.normal_color = GREEN
            self.hover_color = DARK_GREEN
        
        def draw(self, surface):
            mouse_pos = pygame.mouse.get_pos()
            color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.normal_color

            shadow_offset = 5
            shadow_rect = self.rect.move(shadow_offset, shadow_offset)

            pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=10)
            pygame.draw.rect(surface, color, self.rect, border_radius=10)
            pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
            
            text_surf = self.font.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
        
        def is_clicked(self, event):
            return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
        

    start_button = Button(
        SCREEN_WIDTH//2 - 250, 
        SCREEN_HEIGHT//2 - 40, 
        500, 80, 
        "Start The Game"
    )

    running = True
    #current_state = GAME2
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if current_state == MENU:
                if start_button.is_clicked(event):
                    current_state = GAME1
                    try:
                        pygame.mixer.music.load("assets/sounds/background_music.mp3")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)  # music start
                    except:
                        print("Failed to load music") 
        
        if current_state == MENU:
            screen.blit(background, (0, 0))
            start_button.draw(screen)

        elif current_state == GAME1:
            game1.run(event)
            if game1.state == "next_level":
                levels_data["level1"] = {
                    "time_ms": game1.time_used,
                    "coins": game1.coins_collected,
                    "diamonds": game1.diamonds_collected,
                }
                current_state = GAME2

        elif current_state == GAME2:
            game2.run(event)
            if game2.state == "next_level":
                levels_data["level2"] = {
                    "time_ms": game2.time_used,
                    "coins": game2.coins_collected,
                    "diamonds": game2.diamonds_collected,
                }

                summary = GameSummary(screen, levels_data, game1.coins_collected, game2.coins_collected, game1.diamonds_collected, game2.diamonds_collected)

                current_state = SUMMARY
            
        elif current_state == SUMMARY:
            summary.run()

        pygame.display.update()

    pygame.quit()
    sys.exit()