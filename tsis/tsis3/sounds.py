import os
import pygame

SOUNDS = {}
ENABLED = True


def init(enabled):
    global ENABLED
    ENABLED = bool(enabled)
    pygame.mixer.init()
    folder = 'assets'
    files = {
        'engine': 'engine.wav',
        'crash':  'crash.wav',
        'coin':   'coin.wav',
        'nitro':  'nitro.wav',
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


def play(key, loops=0):
    if not ENABLED:
        return
    s = SOUNDS.get(key)
    if s:
        s.play(loops=loops)


def stop(key):
    s = SOUNDS.get(key)
    if s:
        s.stop()


def set_enabled(flag):
    global ENABLED
    ENABLED = bool(flag)
    if not flag:
        for s in SOUNDS.values():
            s.stop()
