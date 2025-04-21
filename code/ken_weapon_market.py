import pygame
import sys

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set.mode((WIDTH, HEIGHT))
pygame.display.set.caption("Weapon Market")
clock = pygame.time.Clock()



running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit