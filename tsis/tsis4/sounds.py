import os
import pygame

SOUNDS = {}
ENABLED = True


def init(enabled):
    global ENABLED
    ENABLED = bool(enabled)
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"err: mixer init failed {e}")
            ENABLED = False
            return
    folder = 'assets'
    files = {
        'eat':       'eat.wav',
        'gameover':  'gameover.wav',
        'powerup':   'powerup.wav',
    }
    for key, name in files.items():
        path = os.path.join(folder, name)
        if os.path.exists(path):
            try:
                SOUNDS[key] = pygame.mixer.Sound(path)
            except pygame.error as e:
                print(f"err: cant load {path}: {e}")
        else:
            print(f"data: missing {path}")


def play(key):
    if not ENABLED:
        return
    s = SOUNDS.get(key)
    if s:
        s.play()


def set_enabled(flag):
    global ENABLED
    ENABLED = bool(flag)
