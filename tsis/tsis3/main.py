import pygame
import sys
import sounds
from racer import GameState, WIDTH, HEIGHT, FINISH_DISTANCE
from persistence import load_settings, save_score
from ui import (main_menu, leaderboard_screen, settings_screen, text_input,
                game_over_screen)

pygame.init()
pygame.mixer.init()
sounds.init(load_settings().get('sound', True))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

font = pygame.font.SysFont('Arial', 22)
big_font = pygame.font.SysFont('Arial', 56, bold=True)
small_font = pygame.font.SysFont('Arial', 16)


def play(username):
    settings = load_settings()
    sounds.set_enabled(settings.get('sound', True))
    state = GameState(settings, username)
    clock = pygame.time.Clock()
    sounds.play('engine', loops=-1)

    while True:
        clock.tick(60)
        ticks = pygame.time.get_ticks()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        state.player.update(keys)
        result = state.update(ticks)

        state.draw(screen)
        screen.blit(small_font.render(f"score: {state.score}", True, (255, 255, 255)), (10, 10))
        screen.blit(small_font.render(f"coins: {state.coins_collected}", True, (255, 215, 0)),
                    (WIDTH - 130, 10))
        screen.blit(small_font.render(f"dist: {state.distance}/{FINISH_DISTANCE}", True, (255, 255, 255)),
                    (10, 32))
        screen.blit(small_font.render(f"name: {username}", True, (200, 200, 200)),
                    (WIDTH - 200, 32))

        if state.active_pu:
            left = max(0, (state.pu_until - ticks) // 1000)
            txt = f"{state.active_pu}"
            if state.active_pu == 'nitro':
                txt += f" {left}s"
            elif state.active_pu == 'shield':
                txt = "shield up"
            screen.blit(small_font.render(txt, True, (255, 255, 0)), (10, 54))

        pygame.display.flip()

        if result in ('crash', 'finish'):
            sounds.stop('engine')
            score = state.score
            if result == 'finish':
                score += 500
            save_score(username, score, state.distance, state.coins_collected)
            choice = game_over_screen(screen, font, big_font,
                                      score, state.distance, state.coins_collected)
            return choice


def loop():
    username = None
    while True:
        choice = main_menu(screen, font, big_font)
        if choice == 'play':
            if not username:
                username = text_input(screen, font, big_font, 'Enter username:')
            while True:
                r = play(username)
                if r == 'retry':
                    continue
                break
        elif choice == 'leaderboard':
            leaderboard_screen(screen, font, big_font)
        elif choice == 'settings':
            settings_screen(screen, font, big_font)
            sounds.set_enabled(load_settings().get('sound', True))


if __name__ == '__main__':
    loop()
