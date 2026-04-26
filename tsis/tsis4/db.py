import psycopg2
from config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""


def conn():
    return psycopg2.connect(**load_config())


def init():
    c = conn()
    cur = c.cursor()
    cur.execute(SCHEMA)
    c.commit()
    cur.close()
    c.close()


def get_or_create_player(username):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    row = cur.fetchone()
    if row:
        pid = row[0]
    else:
        cur.execute("INSERT INTO players(username) VALUES (%s) RETURNING id", (username,))
        pid = cur.fetchone()[0]
        c.commit()
    cur.close()
    c.close()
    return pid


def save_session(username, score, level):
    pid = get_or_create_player(username)
    c = conn()
    cur = c.cursor()
    cur.execute("""INSERT INTO game_sessions(player_id, score, level_reached)
                   VALUES (%s, %s, %s)""", (pid, score, level))
    c.commit()
    cur.close()
    c.close()


def top_scores(limit=10):
    c = conn()
    cur = c.cursor()
    cur.execute("""SELECT p.username, s.score, s.level_reached, s.played_at
                   FROM game_sessions s JOIN players p ON s.player_id=p.id
                   ORDER BY s.score DESC LIMIT %s""", (limit,))
    rows = cur.fetchall()
    cur.close()
    c.close()
    return rows


def personal_best(username):
    c = conn()
    cur = c.cursor()
    cur.execute("""SELECT COALESCE(MAX(s.score), 0)
                   FROM game_sessions s JOIN players p ON s.player_id=p.id
                   WHERE p.username=%s""", (username,))
    row = cur.fetchone()
    cur.close()
    c.close()
    return row[0] if row else 0
