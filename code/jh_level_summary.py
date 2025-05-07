import pygame
import sys

class LevelSummary:
    def __init__(self, screen, level, coins, time_ms):
        self.screen = screen
        self.level = level
        self.coins = coins
        self.time_ms = time_ms
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)
        self.button_rect = pygame.Rect(600, 500, 200, 60)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((10, 10, 30))
            minutes = (self.time_ms // 1000) // 60
            seconds = (self.time_ms // 1000) % 60

            # 显示文字
            level_text = self.font.render(f"Level {self.level} Completed!", True, (255, 255, 0))
            coin_text = self.small_font.render(f"Coins Collected: {self.coins}", True, (255, 255, 255))
            time_text = self.small_font.render(f"Time Taken: {minutes}m {seconds}s", True, (255, 255, 255))
            next_text = self.small_font.render("Next Level", True, (0, 0, 0))

            self.screen.blit(level_text, (450, 200))
            self.screen.blit(coin_text, (530, 280))
            self.screen.blit(time_text, (530, 330))

            # 按钮
            pygame.draw.rect(self.screen, (100, 200, 100), self.button_rect)
            self.screen.blit(next_text, (self.button_rect.x + 35, self.button_rect.y + 15))

            # 检测事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        return "next"  # 返回去主游戏，加载下一关

            pygame.display.flip()
            clock.tick(60)