import pygame
import sys

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800 

class GameSummary:
    def __init__(self, screen, levels_data, game1_coins, game2_coins, game1_diamonds, game2_diamonds):
        self.screen = screen
        self.levels_data = levels_data
        self.game1_coins = game1_coins
        self.game2_coins = game2_coins
        self.game1_diamonds = game1_diamonds
        self.game2_diamonds = game2_diamonds
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)

        self.arrow_img = pygame.image.load("assets/images/arrow1/arrow.png").convert_alpha()
        self.arrow_rect = self.arrow_img.get_rect(topleft=(20, 20))  

        self.background = pygame.image.load('assets/images/good.png').convert()
        self.background = pygame.transform.scale(self.background, (1200, 800))


    def run(self):
        running = True
        while running:
            self.screen.fill((10, 10, 30))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.arrow_img, self.arrow_rect.topleft)

            for level_name, data in self.levels_data.items():
                if level_name == "level1":
                    level_text = self.font.render("Game 1", True, (255, 255, 0))
                    coin_text = self.small_font.render(f"Coins: {data['coins']}", True, (0, 0, 0))
                    diamond_text = self.small_font.render(f"Diamonds: {data['diamonds']}", True, (0, 0, 0))
                    time_text = self.small_font.render(f"Time Taken: {data['time_ms'] // 1000}s", True, (0, 0, 0))
                    self.screen.blit(level_text, (800, 400))
                    self.screen.blit(coin_text, (800, 490))
                    self.screen.blit(diamond_text, (800, 580))
                    self.screen.blit(time_text, (800, 670))
                elif level_name == "level2":
                    level_text = self.font.render("Game 2", True, (255, 255, 0))
                    coin_text = self.small_font.render(f"Coins: {data['coins']}", True, (255, 255, 255))
                    diamond_text = self.small_font.render(f"Diamonds: {data['diamonds']}", True, (255, 255, 255))
                    time_text = self.small_font.render(f"Time Taken: {data['time_ms'] // 1000}s", True, (255, 255, 255))
                    self.screen.blit(level_text, (240, 50))
                    self.screen.blit(coin_text, (240, 140))
                    self.screen.blit(diamond_text, (240, 230))
                    self.screen.blit(time_text, (240, 320))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.arrow_rect.collidepoint(event.pos):
                        return "menu"
