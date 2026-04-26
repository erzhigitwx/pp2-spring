import pygame
import random
import sys
from datetime import datetime

import game as g
import sounds
from db import init as db_init, save_session, top_scores, personal_best


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((g.WIDTH, g.HEIGHT))
pygame.display.set_caption("Snake")
sounds.init(g.load_settings().get('sound', True))

font = pygame.font.SysFont('Arial', 18, bold=True)
big_font = pygame.font.SysFont('Arial', 44, bold=True)
small_font = pygame.font.SysFont('Arial', 14)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
LIGHT = (180, 180, 180)
RED = (220, 30, 30)
YELLOW = (255, 215, 0)


class Button:
    def __init__(self, rect, label):
        self.rect = pygame.Rect(rect)
        self.label = label

    def draw(self, surf, hover):
        pygame.draw.rect(surf, LIGHT if hover else GRAY, self.rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)
        t = font.render(self.label, True, BLACK if hover else WHITE)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def text_input(prompt):
    name = ''
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and name:
                    return name
                if ev.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif ev.unicode and ev.unicode.isprintable() and len(name) < 16:
                    name += ev.unicode
        screen.fill(BLACK)
        t = big_font.render(prompt, True, YELLOW)
        screen.blit(t, t.get_rect(center=(g.WIDTH // 2, 150)))
        t = font.render(name + '|', True, WHITE)
        screen.blit(t, t.get_rect(center=(g.WIDTH // 2, 230)))
        t = small_font.render('Enter to confirm', True, LIGHT)
        screen.blit(t, t.get_rect(center=(g.WIDTH // 2, 280)))
        pygame.display.flip()


def main_menu(username):
    btns = [
        Button((g.WIDTH // 2 - 100, 200, 200, 40), 'Play'),
        Button((g.WIDTH // 2 - 100, 250, 200, 40), 'Leaderboard'),
        Button((g.WIDTH // 2 - 100, 300, 200, 40), 'Settings'),
        Button((g.WIDTH // 2 - 100, 350, 200, 40), 'Quit'),
    ]
    while True:
        mp = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for b in btns:
                    if b.clicked(ev.pos):
                        if b.label == 'Quit':
                            pygame.quit()
                            sys.exit()
                        return b.label.lower()
        screen.fill(BLACK)
        t = big_font.render('SNAKE', True, YELLOW)
        screen.blit(t, t.get_rect(center=(g.WIDTH // 2, 100)))
        t = small_font.render(f'player: {username}', True, LIGHT)
        screen.blit(t, t.get_rect(center=(g.WIDTH // 2, 150)))
        for b in btns:
            b.draw(screen, b.rect.collidepoint(mp))
        pygame.display.flip()


def leaderboard_view():
    rows = top_scores(10)
    back = Button((g.WIDTH // 2 - 60, g.HEIGHT - 60, 120, 35), 'Back')
    while True:
        mp = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and back.clicked(ev.pos):
                return
        screen.fill(BLACK)
        t = big_font.render('TOP 10', True, YELLOW)
        screen.blit(t, t.get_rect(center=(g.WIDTH // 2, 50)))
        if not rows:
            t = font.render('no records yet', True, LIGHT)
            screen.blit(t, t.get_rect(center=(g.WIDTH // 2, 200)))
        else:
            y = 110
            for i, r in enumerate(rows, 1):
                username, score, level, played = r
                date = played.strftime('%Y-%m-%d') if played else '-'
                line = f"{i:>2} {username:<14} sc {score:>4}  lv {level:<2}  {date}"
                screen.blit(font.render(line, True, WHITE), (40, y))
                y += 25
        back.draw(screen, back.rect.collidepoint(mp))
        pygame.display.flip()


def settings_view():
    s = g.load_settings()
    palette = [[0, 180, 0], [220, 30, 30], [50, 100, 220], [255, 215, 0], [180, 50, 200]]

    color_btn = Button((300, 130, 100, 35), 'change')
    grid_btn = Button((300, 180, 100, 35), 'on' if s['grid'] else 'off')
    sound_btn = Button((300, 230, 100, 35), 'on' if s['sound'] else 'off')
    save_btn = Button((g.WIDTH // 2 - 60, g.HEIGHT - 60, 120, 35), 'Save')

    while True:
        mp = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if color_btn.clicked(ev.pos):
                    cur = list(s['snake_color'])
                    idx = palette.index(cur) if cur in palette else 0
                    s['snake_color'] = palette[(idx + 1) % len(palette)]
                elif grid_btn.clicked(ev.pos):
                    s['grid'] = not s['grid']
                    grid_btn.label = 'on' if s['grid'] else 'off'
                elif sound_btn.clicked(ev.pos):
                    s['sound'] = not s['sound']
                    sound_btn.label = 'on' if s['sound'] else 'off'
                elif save_btn.clicked(ev.pos):
                    g.save_settings(s)
                    return
        screen.fill(BLACK)
        t = big_font.render('SETTINGS', True, YELLOW)
        screen.blit(t, t.get_rect(center=(g.WIDTH // 2, 60)))

        labels = [('snake color:', 140), ('grid:', 190), ('sound:', 240)]
        for txt, y in labels:
            screen.blit(font.render(txt, True, WHITE), (140, y))

        pygame.draw.rect(screen, tuple(s['snake_color']), (420, 132, 30, 30))
        pygame.draw.rect(screen, WHITE, (420, 132, 30, 30), 1)

        for b in (color_btn, grid_btn, sound_btn, save_btn):
            b.draw(screen, b.rect.collidepoint(mp))
        pygame.display.flip()


def game_over_view(score, level, best):
    retry = Button((g.WIDTH // 2 - 200, g.HEIGHT // 2 + 60, 180, 40), 'Retry')
    menu = Button((g.WIDTH // 2 + 20, g.HEIGHT // 2 + 60, 180, 40), 'Menu')
    while True:
        mp = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if retry.clicked(ev.pos):
                    return 'retry'
                if menu.clicked(ev.pos):
                    return 'menu'
        overlay = pygame.Surface((g.WIDTH, g.HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        t = big_font.render('GAME OVER', True, RED)
        screen.blit(t, t.get_rect(center=(g.WIDTH // 2, g.HEIGHT // 2 - 90)))
        screen.blit(font.render(f"score: {score}  level: {level}", True, WHITE),
                    (g.WIDTH // 2 - 100, g.HEIGHT // 2 - 30))
        screen.blit(font.render(f"personal best: {best}", True, YELLOW),
                    (g.WIDTH // 2 - 100, g.HEIGHT // 2))
        for b in (retry, menu):
            b.draw(screen, b.rect.collidepoint(mp))
        pygame.display.flip()


def play(username):
    s = g.load_settings()
    sounds.set_enabled(s.get('sound', True))
    snake = [(g.COLS // 2, g.ROWS // 2)]
    direction = (1, 0)
    obstacles = g.make_obstacles(1, snake)
    food = g.spawn_food(snake, obstacles)
    poison = None
    powerup = None
    score = 0
    level = 1
    base_speed = 8
    speed = base_speed
    foods_for_level = 0
    foods_to_next = 4

    speed_mod = 1.0
    speed_until = 0
    shield_on = False
    poison_timer = 0
    pu_timer = 0

    best = personal_best(username)

    clock = pygame.time.Clock()

    while True:
        ticks = pygame.time.get_ticks()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif ev.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif ev.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif ev.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        hit_wall = g.is_wall(*new_head)
        hit_obstacle = new_head in obstacles
        hit_self = new_head in snake

        if hit_wall or hit_obstacle or hit_self:
            if shield_on:
                shield_on = False
                # bounce back - just dont move this tick
                pass
            else:
                sounds.play('gameover')
                save_session(username, score, level)
                return game_over_view(score, level, max(best, score))

        snake.insert(0, new_head)

        ate_food = False
        if new_head == food['pos']:
            sounds.play('eat')
            score += food['points']
            foods_for_level += 1
            if foods_for_level >= foods_to_next:
                level += 1
                foods_for_level = 0
                speed = base_speed + level * 2
                obstacles = g.make_obstacles(level, snake)
                # if food now sits on a new obstacle just respawn
                if food['pos'] in obstacles:
                    food = g.spawn_food(snake, obstacles)
            food = g.spawn_food(snake, obstacles)
            ate_food = True

        if poison and new_head == poison['pos']:
            sounds.play('gameover')
            for _ in range(2):
                if snake:
                    snake.pop()
            poison = None
            if len(snake) <= 1:
                save_session(username, score, level)
                return game_over_view(score, level, max(best, score))

        if powerup and new_head == powerup['pos']:
            sounds.play('powerup')
            kind = powerup['kind']
            if kind == 'speed':
                speed_mod = 1.6
                speed_until = ticks + 5000
            elif kind == 'slow':
                speed_mod = 0.6
                speed_until = ticks + 5000
            elif kind == 'shield':
                shield_on = True
            powerup = None

        if not ate_food:
            snake.pop()

        if food['lifetime'] is not None:
            food['age'] += 1
            if food['age'] >= food['lifetime']:
                food = g.spawn_food(snake, obstacles)

        if poison:
            poison['age'] += 1
            if poison['age'] >= poison['lifetime']:
                poison = None
        else:
            poison_timer += 1
            if poison_timer > 60:
                if random.random() < 0.4:
                    poison = g.spawn_poison(snake, obstacles)
                poison_timer = 0

        if powerup:
            if ticks - powerup['spawn_ms'] > 8000:
                powerup = None
        else:
            pu_timer += 1
            if pu_timer > 80:
                if random.random() < 0.3:
                    powerup = g.spawn_powerup(snake, obstacles, food['pos'])
                pu_timer = 0

        if speed_mod != 1.0 and ticks >= speed_until:
            speed_mod = 1.0

        screen.fill(BLACK)
        if s.get('grid'):
            g.draw_grid(screen)
        g.draw_walls(screen)

        for ox, oy in obstacles:
            pygame.draw.rect(screen, (90, 90, 90), (ox * g.CELL, oy * g.CELL, g.CELL, g.CELL))
            pygame.draw.rect(screen, BLACK, (ox * g.CELL, oy * g.CELL, g.CELL, g.CELL), 1)

        fx, fy = food['pos']
        pygame.draw.rect(screen, food['color'], (fx * g.CELL, fy * g.CELL, g.CELL, g.CELL))
        if food['lifetime']:
            left = max(0, food['lifetime'] - food['age']) / food['lifetime']
            pygame.draw.rect(screen, WHITE, (fx * g.CELL, fy * g.CELL - 4, int(g.CELL * left), 3))

        if poison:
            px, py = poison['pos']
            pygame.draw.rect(screen, poison['color'], (px * g.CELL, py * g.CELL, g.CELL, g.CELL))
            pygame.draw.rect(screen, RED, (px * g.CELL, py * g.CELL, g.CELL, g.CELL), 2)

        if powerup:
            ux, uy = powerup['pos']
            color = g.PU_COLORS[powerup['kind']]
            pygame.draw.rect(screen, color, (ux * g.CELL, uy * g.CELL, g.CELL, g.CELL))
            ch = powerup['kind'][0].upper()
            t = small_font.render(ch, True, BLACK)
            screen.blit(t, t.get_rect(center=(ux * g.CELL + g.CELL // 2,
                                              uy * g.CELL + g.CELL // 2)))

        sn_color = tuple(s['snake_color'])
        for i, seg in enumerate(snake):
            c = sn_color if i > 0 else tuple(max(v - 60, 0) for v in sn_color)
            pygame.draw.rect(screen, c, (seg[0] * g.CELL, seg[1] * g.CELL, g.CELL, g.CELL))
            pygame.draw.rect(screen, BLACK, (seg[0] * g.CELL, seg[1] * g.CELL, g.CELL, g.CELL), 1)

        info_y = g.ROWS * g.CELL + 6
        screen.blit(font.render(f"sc {score}", True, WHITE), (10, info_y))
        screen.blit(font.render(f"lv {level}", True, WHITE), (90, info_y))
        screen.blit(font.render(f"sp {speed}", True, WHITE), (160, info_y))
        screen.blit(font.render(f"best {max(best, score)}", True, YELLOW), (240, info_y))
        if shield_on:
            screen.blit(small_font.render('shield', True, WHITE), (380, info_y + 2))
        if speed_mod != 1.0:
            mark = 'fast' if speed_mod > 1 else 'slow'
            screen.blit(small_font.render(mark, True, YELLOW), (440, info_y + 2))

        pygame.display.flip()
        clock.tick(int(speed * speed_mod))


def loop():
    db_init()
    username = text_input('enter username:')
    while True:
        choice = main_menu(username)
        if choice == 'play':
            while True:
                r = play(username)
                if r == 'retry':
                    continue
                break
        elif choice == 'leaderboard':
            leaderboard_view()
        elif choice == 'settings':
            settings_view()
            sounds.set_enabled(g.load_settings().get('sound', True))


if __name__ == '__main__':
    loop()
