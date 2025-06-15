def platform_map(username):
    import pygame
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

    # let Game1 and Game2
    game1 = Game1(screen, username)
    game2 = Game2(screen, username)

    # save data 
    levels_data = {}

    summary = None
    current_state = MENU

    class Button:
        def __init__(self, x, y, width, height, text):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)
            self.normal_color = GREEN
            self.hover_color = DARK_GREEN
            
        def draw(self, surface):
            mouse_pos = pygame.mouse.get_pos()
            color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.normal_color

            pygame.draw.rect(surface, (50, 50, 50), self.rect.move(5,5), border_radius=10)
            pygame.draw.rect(surface, color, self.rect, border_radius=10)
            pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
                
            text_surf = self.font.render(self.text, True, BLACK) # print word
            text_rect = text_surf.get_rect(center=self.rect.center) # centre
            surface.blit(text_surf, text_rect) # got word
            
        def is_clicked(self, event):
            return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
            
    start_button = Button(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 40, 500, 80, "Start The Game")

    running = True
    #current_state = GAME2
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False

            if current_state == MENU and start_button.is_clicked(event):
                current_state = GAME1
                try:
                    pygame.mixer.music.load("assets/sounds/background_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1) # loop the music
                except:
                    print("Failed to load music")

        if current_state == MENU:
            screen.blit(background, (0, 0))
            start_button.draw(screen)

        elif current_state == GAME1:
            game1.run(event)
            if game1.state == "next_level":
                levels_data["level1"] = {
                    "coins": game1.coins_collected,
                    "diamonds": game1.diamonds_collected,
                }
                current_state = GAME2

        elif current_state == GAME2:
            game2.run(event)
            if game2.state == "next_level":
                levels_data["level2"] = {
                    "coins": game2.coins_collected,
                    "diamonds": game2.diamonds_collected,
                }
                summary = GameSummary(screen, levels_data, game1.coins_collected, game2.coins_collected, game1.diamonds_collected, game2.diamonds_collected)
                current_state = SUMMARY
            
        elif current_state == SUMMARY:
            result = summary.run()
            if result == "menu":
                   pygame.mixer.music.stop()
                   current_state = MENU

        pygame.display.update() # actually same with pygame.display.flip() function

    pygame.mixer.music.stop()
    return  # Start the game → Show menu Click → the button → First level (Game1) → Next level → Second level (Game2) → End the game → Results summary page → Click the button to return to the main menu