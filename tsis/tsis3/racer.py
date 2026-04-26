import pygame
import random
import sounds


WIDTH, HEIGHT = 500, 700
ROAD_LEFT, ROAD_RIGHT = 100, 400
LANE_W = (ROAD_RIGHT - ROAD_LEFT) // 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 30, 30)
GREEN = (0, 200, 0)
BLUE = (50, 100, 220)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (180, 50, 200)
GRAY = (50, 50, 50)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

CAR_COLORS = {'green': GREEN, 'red': RED, 'blue': BLUE, 'yellow': YELLOW}

DIFFICULTY = {
    'easy':   {'enemy_speed': 2, 'enemy_rate': 80, 'obstacle_rate': 200},
    'normal': {'enemy_speed': 3, 'enemy_rate': 60, 'obstacle_rate': 150},
    'hard':   {'enemy_speed': 4, 'enemy_rate': 45, 'obstacle_rate': 100},
}

COIN_TYPES = [
    {'color': BRONZE, 'value': 1, 'weight': 60, 'r': 10},
    {'color': SILVER, 'value': 2, 'weight': 30, 'r': 12},
    {'color': YELLOW, 'value': 5, 'weight': 10, 'r': 14},
]

POWERUPS = ['nitro', 'shield', 'repair']
PU_COLORS = {'nitro': ORANGE, 'shield': BLUE, 'repair': GREEN}

FINISH_DISTANCE = 5000


def lane_x(lane):
    return ROAD_LEFT + lane * LANE_W + LANE_W // 2


class Player:
    def __init__(self, color):
        self.w, self.h = 40, 60
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 90
        self.color = color
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT + 5:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.w < ROAD_RIGHT - 5:
            self.x += self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surf, BLACK, (self.x, self.y, self.w, self.h), 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Enemy:
    def __init__(self, speed, lane=None):
        if lane is None:
            lane = random.randint(0, 2)
        self.w, self.h = 40, 60
        self.x = lane_x(lane) - self.w // 2
        self.y = -self.h
        self.speed = speed

    def update(self):
        self.y += self.speed

    def off(self):
        return self.y > HEIGHT

    def draw(self, surf):
        pygame.draw.rect(surf, RED, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surf, BLACK, (self.x, self.y, self.w, self.h), 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Obstacle:
    # types: oil, barrier, bump
    def __init__(self, kind, speed):
        self.kind = kind
        lane = random.randint(0, 2)
        self.x = lane_x(lane) - 18
        self.y = -40
        self.w, self.h = 36, 36
        self.speed = speed

    def update(self):
        self.y += self.speed

    def off(self):
        return self.y > HEIGHT

    def draw(self, surf):
        if self.kind == 'oil':
            pygame.draw.ellipse(surf, BLACK, (self.x, self.y, self.w, self.h))
        elif self.kind == 'barrier':
            pygame.draw.rect(surf, ORANGE, (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surf, BLACK, (self.x, self.y, self.w, self.h), 2)
        elif self.kind == 'bump':
            pygame.draw.rect(surf, YELLOW, (self.x, self.y - 6, self.w, 12))
            pygame.draw.rect(surf, BLACK, (self.x, self.y - 6, self.w, 12), 1)
        elif self.kind == 'nitro_strip':
            pygame.draw.rect(surf, BLUE, (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surf, WHITE, (self.x, self.y, self.w, self.h), 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


def pick_coin():
    total = sum(c['weight'] for c in COIN_TYPES)
    r = random.randint(1, total)
    a = 0
    for c in COIN_TYPES:
        a += c['weight']
        if r <= a:
            return c
    return COIN_TYPES[0]


class Coin:
    def __init__(self, speed):
        t = pick_coin()
        lane = random.randint(0, 2)
        self.x = lane_x(lane)
        self.y = -t['r'] * 2
        self.r = t['r']
        self.color = t['color']
        self.value = t['value']
        self.speed = speed

    def update(self):
        self.y += self.speed

    def off(self):
        return self.y > HEIGHT

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(surf, BLACK, (self.x, self.y), self.r, 2)

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)


class PowerUp:
    def __init__(self, kind, speed):
        self.kind = kind
        lane = random.randint(0, 2)
        self.x = lane_x(lane)
        self.y = -20
        self.r = 14
        self.speed = speed
        self.life = 600  # ticks before it vanishes

    def update(self):
        self.y += self.speed
        self.life -= 1

    def off(self):
        return self.y > HEIGHT or self.life <= 0

    def draw(self, surf):
        pygame.draw.circle(surf, PU_COLORS[self.kind], (self.x, self.y), self.r)
        pygame.draw.circle(surf, WHITE, (self.x, self.y), self.r, 2)
        font = pygame.font.SysFont('Arial', 14, bold=True)
        ch = self.kind[0].upper()
        t = font.render(ch, True, WHITE)
        surf.blit(t, t.get_rect(center=(self.x, self.y)))

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)


class GameState:
    def __init__(self, settings, username):
        self.username = username
        d = DIFFICULTY[settings['difficulty']]
        self.enemy_speed = d['enemy_speed']
        self.enemy_rate = d['enemy_rate']
        self.obstacle_rate = d['obstacle_rate']
        self.player = Player(CAR_COLORS[settings['car_color']])
        self.enemies = []
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.score = 0
        self.coins_collected = 0
        self.distance = 0
        self.stripe = 0
        self.enemy_t = 0
        self.coin_t = 0
        self.obstacle_t = 0
        self.pu_t = 0
        # active power-up info
        self.active_pu = None
        self.pu_until = 0
        self.shield_on = False

    def speedup_check(self):
        # bump enemy speed every 10 coins
        target = 1 + self.coins_collected // 10
        self.enemy_speed = DIFFICULTY['normal']['enemy_speed'] + target

    def safe_lane(self):
        # try to spawn away from player lane to avoid unfair hits
        px = self.player.x + self.player.w // 2
        plane = (px - ROAD_LEFT) // LANE_W
        choices = [l for l in range(3) if l != plane]
        return random.choice(choices)

    def spawn_enemy(self):
        self.enemies.append(Enemy(self.enemy_speed, self.safe_lane()))

    def spawn_obstacle(self):
        kinds = ['oil', 'barrier', 'bump', 'nitro_strip']
        weights = [3, 2, 3, 1]
        kind = random.choices(kinds, weights=weights)[0]
        self.obstacles.append(Obstacle(kind, self.enemy_speed))

    def spawn_coin(self):
        self.coins.append(Coin(self.enemy_speed))

    def spawn_powerup(self):
        if not self.active_pu:
            self.powerups.append(PowerUp(random.choice(POWERUPS), self.enemy_speed))

    def update(self, ticks):
        self.distance += 1
        self.score += 1
        self.stripe = (self.stripe + self.enemy_speed) % 40

        self.enemy_t += 1
        if self.enemy_t >= self.enemy_rate:
            self.spawn_enemy()
            self.enemy_t = 0

        self.obstacle_t += 1
        if self.obstacle_t >= self.obstacle_rate:
            self.spawn_obstacle()
            self.obstacle_t = 0

        self.coin_t += 1
        if self.coin_t >= 90 + random.randint(0, 60):
            self.spawn_coin()
            self.coin_t = 0

        self.pu_t += 1
        if self.pu_t >= 600:
            self.spawn_powerup()
            self.pu_t = 0

        for e in self.enemies: e.update()
        for o in self.obstacles: o.update()
        for c in self.coins: c.update()
        for p in self.powerups: p.update()

        self.enemies = [e for e in self.enemies if not e.off()]
        self.obstacles = [o for o in self.obstacles if not o.off()]
        self.powerups = [p for p in self.powerups if not p.off()]

        if self.active_pu and ticks >= self.pu_until:
            if self.active_pu == 'nitro':
                self.enemy_speed -= 3
            self.active_pu = None

        pr = self.player.rect()
        for e in self.enemies:
            if pr.colliderect(e.rect()):
                if self.shield_on:
                    self.shield_on = False
                    self.enemies.remove(e)
                else:
                    sounds.play('crash')
                    return 'crash'

        for o in list(self.obstacles):
            if pr.colliderect(o.rect()):
                if o.kind == 'oil':
                    # slip - randomize x slightly
                    self.player.x += random.choice([-15, 15])
                    self.obstacles.remove(o)
                elif o.kind == 'barrier':
                    if self.shield_on:
                        self.shield_on = False
                        self.obstacles.remove(o)
                    else:
                        sounds.play('crash')
                        return 'crash'
                elif o.kind == 'bump':
                    self.score += 5
                    self.obstacles.remove(o)
                elif o.kind == 'nitro_strip':
                    self.active_pu = 'nitro'
                    self.pu_until = ticks + 3000
                    self.enemy_speed += 3
                    self.obstacles.remove(o)
                    sounds.play('nitro')

        kept = []
        for c in self.coins:
            if pr.colliderect(c.rect()):
                self.coins_collected += c.value
                self.speedup_check()
                sounds.play('coin')
            elif not c.off():
                kept.append(c)
        self.coins = kept

        kept = []
        for p in self.powerups:
            if pr.colliderect(p.rect()):
                if p.kind == 'shield':
                    self.shield_on = True
                    self.active_pu = 'shield'
                    self.pu_until = 10**12  # last till hit
                    sounds.play('nitro')
                elif p.kind == 'nitro':
                    self.active_pu = 'nitro'
                    self.pu_until = ticks + 4000
                    self.enemy_speed += 3
                    sounds.play('nitro')
                elif p.kind == 'repair':
                    if self.obstacles:
                        self.obstacles.pop(0)
                    self.active_pu = 'repair'
                    self.pu_until = ticks + 100
            else:
                kept.append(p)
        self.powerups = kept

        if self.distance >= FINISH_DISTANCE:
            return 'finish'
        return None

    def draw(self, surf):
        surf.fill(GREEN)
        pygame.draw.rect(surf, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
        pygame.draw.line(surf, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 3)
        pygame.draw.line(surf, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 3)
        for lane in range(1, 3):
            x = ROAD_LEFT + lane * LANE_W
            for y in range(-20 + int(self.stripe), HEIGHT, 40):
                pygame.draw.line(surf, WHITE, (x, y), (x, y + 20), 2)

        for o in self.obstacles: o.draw(surf)
        for c in self.coins: c.draw(surf)
        for p in self.powerups: p.draw(surf)
        for e in self.enemies: e.draw(surf)
        self.player.draw(surf)
