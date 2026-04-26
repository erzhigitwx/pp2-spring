import json
import os

SETTINGS_FILE = 'settings.json'
LEADERBOARD_FILE = 'leaderboard.json'

DEFAULT_SETTINGS = {
    'sound': True,
    'car_color': 'green',
    'difficulty': 'normal',
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_FILE) as f:
            data = json.load(f)
        # fill missing keys
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(s):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, indent=2)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def save_score(name, score, distance, coins):
    board = load_leaderboard()
    board.append({'name': name, 'score': score, 'distance': distance, 'coins': coins})
    board.sort(key=lambda x: x['score'], reverse=True)
    board = board[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(board, f, indent=2)
    return board
