import pygame
import sys
from persistence import load_leaderboard, load_settings, save_settings


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
LIGHT = (180, 180, 180)
GREEN = (0, 200, 0)
RED = (220, 30, 30)
BLUE = (50, 100, 220)
YELLOW = (255, 215, 0)


class Button:
    def __init__(self, rect, label):
        self.rect = pygame.Rect(rect)
        self.label = label

    def draw(self, surf, font, hover):
        bg = LIGHT if hover else GRAY
        pygame.draw.rect(surf, bg, self.rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)
        t = font.render(self.label, True, WHITE if not hover else BLACK)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def title_text(surf, font, text, y, color=WHITE):
    t = font.render(text, True, color)
    surf.blit(t, t.get_rect(center=(surf.get_width() // 2, y)))


def main_menu(screen, font, big_font):
    w, h = screen.get_size()
    btns = [
        Button((w // 2 - 100, 200, 200, 50), 'Play'),
        Button((w // 2 - 100, 270, 200, 50), 'Leaderboard'),
        Button((w // 2 - 100, 340, 200, 50), 'Settings'),
        Button((w // 2 - 100, 410, 200, 50), 'Quit'),
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
        title_text(screen, big_font, 'RACER', 100, YELLOW)
        for b in btns:
            b.draw(screen, font, b.rect.collidepoint(mp))
        pygame.display.flip()


def text_input(screen, font, big_font, prompt):
    name = ''
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and name:
                    return name
                elif ev.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif ev.unicode and ev.unicode.isprintable() and len(name) < 16:
                    name += ev.unicode

        screen.fill(BLACK)
        title_text(screen, big_font, prompt, 200, YELLOW)
        title_text(screen, font, name + '|', 280, WHITE)
        title_text(screen, font, 'Enter to confirm', 340, LIGHT)
        pygame.display.flip()


def leaderboard_screen(screen, font, big_font):
    board = load_leaderboard()
    back = Button((screen.get_width() // 2 - 60, screen.get_height() - 70, 120, 40), 'Back')
    while True:
        mp = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and back.clicked(ev.pos):
                return

        screen.fill(BLACK)
        title_text(screen, big_font, 'TOP 10', 60, YELLOW)
        if not board:
            title_text(screen, font, 'no records yet', 200, LIGHT)
        else:
            y = 130
            for i, r in enumerate(board, 1):
                line = f"{i:>2}. {r['name']:<14} {r['score']:>5}  d:{r['distance']}  c:{r['coins']}"
                t = font.render(line, True, WHITE)
                screen.blit(t, (screen.get_width() // 2 - 200, y))
                y += 30
        back.draw(screen, font, back.rect.collidepoint(mp))
        pygame.display.flip()


def settings_screen(screen, font, big_font):
    s = load_settings()
    colors = ['green', 'red', 'blue', 'yellow']
    diffs = ['easy', 'normal', 'hard']

    sound_btn = Button((400, 150, 100, 40), 'on' if s['sound'] else 'off')
    color_btn = Button((400, 220, 100, 40), s['car_color'])
    diff_btn = Button((400, 290, 100, 40), s['difficulty'])
    save_btn = Button((screen.get_width() // 2 - 60, screen.get_height() - 70, 120, 40), 'Save')

    while True:
        mp = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.clicked(ev.pos):
                    s['sound'] = not s['sound']
                    sound_btn.label = 'on' if s['sound'] else 'off'
                elif color_btn.clicked(ev.pos):
                    i = colors.index(s['car_color'])
                    s['car_color'] = colors[(i + 1) % len(colors)]
                    color_btn.label = s['car_color']
                elif diff_btn.clicked(ev.pos):
                    i = diffs.index(s['difficulty'])
                    s['difficulty'] = diffs[(i + 1) % len(diffs)]
                    diff_btn.label = s['difficulty']
                elif save_btn.clicked(ev.pos):
                    save_settings(s)
                    return

        screen.fill(BLACK)
        title_text(screen, big_font, 'SETTINGS', 60, YELLOW)
        labels = [('Sound:', 160), ('Car color:', 230), ('Difficulty:', 300)]
        for txt, y in labels:
            t = font.render(txt, True, WHITE)
            screen.blit(t, (200, y))
        for b in (sound_btn, color_btn, diff_btn, save_btn):
            b.draw(screen, font, b.rect.collidepoint(mp))
        pygame.display.flip()


def game_over_screen(screen, font, big_font, score, distance, coins):
    retry = Button((screen.get_width() // 2 - 220, 400, 180, 50), 'Retry')
    menu = Button((screen.get_width() // 2 + 40, 400, 180, 50), 'Main Menu')
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

        screen.fill(BLACK)
        title_text(screen, big_font, 'GAME OVER', 120, RED)
        title_text(screen, font, f"Score: {score}", 220, WHITE)
        title_text(screen, font, f"Distance: {distance}", 260, WHITE)
        title_text(screen, font, f"Coins: {coins}", 300, YELLOW)
        for b in (retry, menu):
            b.draw(screen, font, b.rect.collidepoint(mp))
        pygame.display.flip()
