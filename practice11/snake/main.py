import pygame
import random
import sys

pygame.init()

CELL = 20
COLS, ROWS = 30, 25
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 30, 30)
GRAY = (40, 40, 40)
ORANGE = (255, 140, 0)
PURPLE = (180, 50, 200)

font = pygame.font.SysFont('Arial', 20, bold=True)

# red stays, others dissapear after some ticks
FOOD_TYPES = [
    {'color': RED, 'points': 1, 'weight': 70, 'lifetime': None},
    {'color': ORANGE, 'points': 3, 'weight': 25, 'lifetime': 60},
    {'color': PURPLE, 'points': 5, 'weight': 5, 'lifetime': 35},
]


def draw_walls():
    for x in range(COLS):
        pygame.draw.rect(screen, GRAY, (x * CELL, 0, CELL, CELL))
        pygame.draw.rect(screen, GRAY, (x * CELL, (ROWS - 1) * CELL, CELL, CELL))
    for y in range(ROWS):
        pygame.draw.rect(screen, GRAY, (0, y * CELL, CELL, CELL))
        pygame.draw.rect(screen, GRAY, ((COLS - 1) * CELL, y * CELL, CELL, CELL))


def is_wall(x, y):
    return x <= 0 or x >= COLS - 1 or y <= 0 or y >= ROWS - 1


def pick_food_type():
    total = sum(f['weight'] for f in FOOD_TYPES)
    r = random.randint(1, total)
    acc = 0
    for f in FOOD_TYPES:
        acc += f['weight']
        if r <= acc:
            return f
    return FOOD_TYPES[0]


def spawn_food(snake_body):
    while True:
        x = random.randint(2, COLS - 3)
        y = random.randint(2, ROWS - 3)
        if (x, y) not in snake_body and not is_wall(x, y):
            t = pick_food_type()
            return {
                'pos': (x, y),
                'color': t['color'],
                'points': t['points'],
                'lifetime': t['lifetime'],  # None means it never expires
                'age': 0,
            }


def run():
    clock = pygame.time.Clock()

    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    food = spawn_food(snake)
    score = 0
    level = 1
    base_speed = 8
    speed = base_speed
    food_for_level = 0
    foods_to_next = 4

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        if is_wall(new_head[0], new_head[1]) or new_head in snake:
            if game_over(score, level):
                return run()

        snake.insert(0, new_head)

        # if timer runs out and snake didnt eat it, just spawn new one
        if food['lifetime'] is not None:
            food['age'] += 1
            if food['age'] >= food['lifetime'] and new_head != food['pos']:
                food = spawn_food(snake)

        if new_head == food['pos']:
            score += food['points']
            food_for_level += 1
            if food_for_level >= foods_to_next:
                level += 1
                food_for_level = 0
                speed = base_speed + level * 2
            food = spawn_food(snake)
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_walls()

        fx, fy = food['pos']
        pygame.draw.rect(screen, food['color'], (fx * CELL, fy * CELL, CELL, CELL))
        # small timer bar on top of the food
        if food['lifetime'] is not None:
            left = max(0, food['lifetime'] - food['age']) / food['lifetime']
            bar_w = int(CELL * left)
            pygame.draw.rect(screen, WHITE, (fx * CELL, fy * CELL - 4, bar_w, 3))

        for i, seg in enumerate(snake):
            color = GREEN if i > 0 else DARK_GREEN
            pygame.draw.rect(screen, color,
                             (seg[0] * CELL, seg[1] * CELL, CELL, CELL))
            pygame.draw.rect(screen, BLACK,
                             (seg[0] * CELL, seg[1] * CELL, CELL, CELL), 1)

        info_y = ROWS * CELL + 8
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, info_y))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (140, info_y))
        screen.blit(font.render(f"Speed: {speed}", True, WHITE), (270, info_y))
        progress = f"Food: {food_for_level}/{foods_to_next}"
        screen.blit(font.render(progress, True, WHITE), (410, info_y))

        pygame.display.flip()
        clock.tick(speed)


def game_over(score, level):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    big_font = pygame.font.SysFont('Arial', 40, bold=True)
    screen.blit(big_font.render("GAME OVER", True, RED),
                (WIDTH // 2 - 120, HEIGHT // 2 - 60))
    screen.blit(font.render(f"Score: {score}  Level: {level}", True, WHITE),
                (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(font.render("R - Restart  Q - Quit", True, WHITE),
                (WIDTH // 2 - 110, HEIGHT // 2 + 40))
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


if __name__ == '__main__':
    run()
