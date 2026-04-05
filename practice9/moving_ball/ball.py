import pygame


class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

    def move(self, dx, dy, screen_w, screen_h):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if self.radius <= new_x <= screen_w - self.radius:
            self.x = new_x
        if self.radius <= new_y <= screen_h - self.radius:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
