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



running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    coins_text = font.render(f"Coins : {player_coins}", True, (0, 255, 0))
    gems_text = font.render(f"Gems : {player_gems}", True, (150, 0, 150))
    screen.blit(coins_text, (30, 20))
    screen.blit(gems_text, (30, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit