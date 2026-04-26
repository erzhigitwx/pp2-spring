import pygame
import random
import json
import os

CELL = 20
COLS, ROWS = 30, 25
INFO_H = 50
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + INFO_H

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 30, 30)
GRAY = (40, 40, 40)
ORANGE = (255, 140, 0)
PURPLE = (180, 50, 200)
DARK_RED = (130, 0, 0)
BLUE = (50, 100, 220)
YELLOW = (255, 215, 0)
GRID = (25, 25, 25)

SETTINGS_FILE = 'settings.json'

FOOD_TYPES = [
    {'color': RED, 'points': 1, 'weight': 70, 'lifetime': None},
    {'color': ORANGE, 'points': 3, 'weight': 25, 'lifetime': 60},
    {'color': PURPLE, 'points': 5, 'weight': 5, 'lifetime': 35},
]


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        s = {'snake_color': [0, 180, 0], 'grid': True, 'sound': True}
        save_settings(s)
        return s
    with open(SETTINGS_FILE) as f:
        return json.load(f)


def save_settings(s):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, indent=2)


def is_wall(x, y):
    return x <= 0 or x >= COLS - 1 or y <= 0 or y >= ROWS - 1


def pick_food():
    total = sum(f['weight'] for f in FOOD_TYPES)
    r = random.randint(1, total)
    a = 0
    for f in FOOD_TYPES:
        a += f['weight']
        if r <= a:
            return f
    return FOOD_TYPES[0]


def free_cell(snake, blocked):
    while True:
        x = random.randint(2, COLS - 3)
        y = random.randint(2, ROWS - 3)
        if (x, y) not in snake and (x, y) not in blocked and not is_wall(x, y):
            return (x, y)


def spawn_food(snake, obstacles):
    t = pick_food()
    return {
        'pos': free_cell(snake, obstacles),
        'color': t['color'],
        'points': t['points'],
        'lifetime': t['lifetime'],
        'age': 0,
        'poison': False,
    }


def spawn_poison(snake, obstacles):
    return {
        'pos': free_cell(snake, obstacles),
        'color': DARK_RED,
        'points': 0,
        'lifetime': 80,
        'age': 0,
        'poison': True,
    }


# blocks of walls inside the arena, starting from level 3
def make_obstacles(level, snake):
    blocks = set()
    if level < 3:
        return blocks
    count = 4 + (level - 3) * 2
    head = snake[0]
    for _ in range(count * 3):
        x = random.randint(2, COLS - 3)
        y = random.randint(2, ROWS - 3)
        if (x, y) in snake:
            continue
        # dont put block right next to head, snake needs space
        if abs(x - head[0]) <= 1 and abs(y - head[1]) <= 1:
            continue
        blocks.add((x, y))
        if len(blocks) >= count:
            break
    return blocks


POWERUP_TYPES = ['speed', 'slow', 'shield']
PU_COLORS = {'speed': YELLOW, 'slow': BLUE, 'shield': WHITE}


def spawn_powerup(snake, obstacles, food_pos):
    blocked = obstacles | {food_pos}
    return {
        'pos': free_cell(snake, blocked),
        'kind': random.choice(POWERUP_TYPES),
        'spawn_ms': pygame.time.get_ticks(),
    }


def draw_grid(screen):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, ROWS * CELL))
    for y in range(0, ROWS * CELL, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))


def draw_walls(screen):
    for x in range(COLS):
        pygame.draw.rect(screen, GRAY, (x * CELL, 0, CELL, CELL))
        pygame.draw.rect(screen, GRAY, (x * CELL, (ROWS - 1) * CELL, CELL, CELL))
    for y in range(ROWS):
        pygame.draw.rect(screen, GRAY, (0, y * CELL, CELL, CELL))
        pygame.draw.rect(screen, GRAY, ((COLS - 1) * CELL, y * CELL, CELL, CELL))
