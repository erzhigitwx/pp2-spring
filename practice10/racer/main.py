import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 215, 0)
ROAD_COLOR = (50, 50, 50)

font = pygame.font.SysFont('Arial', 30, bold=True)
small_font = pygame.font.SysFont('Arial', 22)

PLAYER_W, PLAYER_H = 40, 60
ENEMY_W, ENEMY_H = 40, 60
COIN_RADIUS = 12

ROAD_LEFT = 80
ROAD_RIGHT = WIDTH - 80
LANE_WIDTH = (ROAD_RIGHT - ROAD_LEFT) // 3


class Player:
    def __init__(self):
        self.w = PLAYER_W
        self.h = PLAYER_H
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - self.h - 20
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT + 5:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.w < ROAD_RIGHT - 5:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.w, self.h), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Enemy:
    def __init__(self, speed):
        lane = random.randint(0, 2)
        self.w = ENEMY_W
        self.h = ENEMY_H
        self.x = ROAD_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - self.w) // 2
        self.y = -self.h
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.w, self.h), 2)

    def off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Coin:
    def __init__(self, speed):
        lane = random.randint(0, 2)
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = -COIN_RADIUS * 2
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), COIN_RADIUS)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), COIN_RADIUS, 2)

    def off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x - COIN_RADIUS, self.y - COIN_RADIUS,
                           COIN_RADIUS * 2, COIN_RADIUS * 2)


def draw_road(stripe_offset):
    screen.fill(GREEN)
    pygame.draw.rect(screen, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 3)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 3)
    for lane in range(1, 3):
        x = ROAD_LEFT + lane * LANE_WIDTH
        for y in range(-20 + stripe_offset, HEIGHT, 40):
            pygame.draw.line(screen, WHITE, (x, y), (x, y + 20), 2)


def show_text(text, x, y, color=WHITE, f=None):
    if f is None:
        f = font
    surf = f.render(text, True, color)
    screen.blit(surf, (x, y))


def game_over_screen(score, coins):
    screen.fill(BLACK)
    show_text("GAME OVER", WIDTH // 2 - 100, HEIGHT // 2 - 60)
    show_text(f"Score: {score}", WIDTH // 2 - 70, HEIGHT // 2)
    show_text(f"Coins: {coins}", WIDTH // 2 - 70, HEIGHT // 2 + 40)
    show_text("R - Restart  Q - Quit", WIDTH // 2 - 150, HEIGHT // 2 + 100, f=small_font)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def run():
    clock = pygame.time.Clock()
    player = Player()
    enemies = []
    coins_list = []
    score = 0
    coins_collected = 0
    enemy_speed = 3
    enemy_timer = 0
    coin_timer = 0
    stripe_offset = 0

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys)

        enemy_timer += 1
        if enemy_timer >= 60:
            enemies.append(Enemy(enemy_speed))
            enemy_timer = 0

        coin_timer += 1
        if coin_timer >= 120 + random.randint(0, 60):
            coins_list.append(Coin(enemy_speed))
            coin_timer = 0

        for e in enemies:
            e.move()
        for c in coins_list:
            c.move()

        enemies = [e for e in enemies if not e.off_screen()]

        player_rect = player.get_rect()
        for e in enemies:
            if player_rect.colliderect(e.get_rect()):
                if game_over_screen(score, coins_collected):
                    return run()

        new_coins = []
        for c in coins_list:
            if player_rect.colliderect(c.get_rect()):
                coins_collected += 1
            elif not c.off_screen():
                new_coins.append(c)
        coins_list = new_coins

        score += 1
        if score % 500 == 0:
            enemy_speed += 0.5

        stripe_offset = (stripe_offset + enemy_speed) % 40
        draw_road(int(stripe_offset))
        player.draw()
        for e in enemies:
            e.draw()
        for c in coins_list:
            c.draw()

        show_text(f"Score: {score}", 10, 10)
        show_text(f"Coins: {coins_collected}", WIDTH - 160, 10, YELLOW)

        pygame.display.flip()


if __name__ == '__main__':
    run()
