import pygame
from clock import Clock

pygame.init()

WIDTH, HEIGHT = 500, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

clock = Clock((WIDTH // 2, HEIGHT // 2 - 30), 180)
fps = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((230, 230, 230))
    clock.draw(screen)
    pygame.display.flip()
    fps.tick(30)

pygame.quit()
