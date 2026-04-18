import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 900, 620
TOOLBAR_H = 60
CANVAS_Y = TOOLBAR_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (60, 60, 60)

font = pygame.font.SysFont('Arial', 13)

COLORS = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, WHITE]

TOOL_PEN = 'Pen'
TOOL_RECT = 'Rect'
TOOL_SQUARE = 'Square'
TOOL_CIRCLE = 'Circle'
TOOL_RTRI = 'RTri'
TOOL_ETRI = 'ETri'
TOOL_RHOMB = 'Rhomb'
TOOL_ERASER = 'Eraser'
TOOLS = [TOOL_PEN, TOOL_RECT, TOOL_SQUARE, TOOL_CIRCLE,
         TOOL_RTRI, TOOL_ETRI, TOOL_RHOMB, TOOL_ERASER]

SHAPE_TOOLS = {TOOL_RECT, TOOL_SQUARE, TOOL_CIRCLE,
               TOOL_RTRI, TOOL_ETRI, TOOL_RHOMB}

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill(WHITE)

current_color = BLACK
current_tool = TOOL_PEN
brush_size = 3
drawing = False
start_pos = None


# take shorter side so its actualy a square
def square_rect(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = min(abs(dx), abs(dy))
    sx = start[0] + (side if dx >= 0 else -side)
    sy = start[1] + (side if dy >= 0 else -side)
    x = min(start[0], sx)
    y = min(start[1], sy)
    return pygame.Rect(x, y, side, side)


def right_triangle_points(start, end):
    # 90 deg corner is at start
    return [start, (end[0], start[1]), (end[0], end[1])]


# height = width * sqrt(3)/2
def equilateral_triangle_points(start, end):
    width = abs(end[0] - start[0])
    x_left = min(start[0], end[0])
    height = width * math.sqrt(3) / 2
    y_base = max(start[1], end[1])
    # drag up -> points up, drag down -> points down
    going_up = end[1] < start[1]
    if going_up:
        return [(x_left, y_base),
                (x_left + width, y_base),
                (x_left + width / 2, y_base - height)]
    else:
        y_top = min(start[1], end[1])
        return [(x_left, y_top + height),
                (x_left + width, y_top + height),
                (x_left + width / 2, y_top)]


def rhombus_points(start, end):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return [(cx, min(y1, y2)),
            (max(x1, x2), cy),
            (cx, max(y1, y2)),
            (min(x1, x2), cy)]


def draw_shape(surface, tool, color, start, end, width):
    if tool == TOOL_RECT:
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = abs(end[0] - start[0])
        h = abs(end[1] - start[1])
        pygame.draw.rect(surface, color, (x, y, w, h), width)
    elif tool == TOOL_SQUARE:
        pygame.draw.rect(surface, color, square_rect(start, end), width)
    elif tool == TOOL_CIRCLE:
        cx = (start[0] + end[0]) // 2
        cy = (start[1] + end[1]) // 2
        r = max(abs(end[0] - start[0]), abs(end[1] - start[1])) // 2
        if r > 0:
            pygame.draw.circle(surface, color, (cx, cy), r, width)
    elif tool == TOOL_RTRI:
        pts = right_triangle_points(start, end)
        pygame.draw.polygon(surface, color, pts, width)
    elif tool == TOOL_ETRI:
        pts = equilateral_triangle_points(start, end)
        pygame.draw.polygon(surface, color, pts, width)
    elif tool == TOOL_RHOMB:
        pts = rhombus_points(start, end)
        pygame.draw.polygon(surface, color, pts, width)


def draw_toolbar():
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, TOOLBAR_H))

    x = 10
    for tool in TOOLS:
        rect = pygame.Rect(x, 8, 58, 22)
        bg = WHITE if tool == current_tool else GRAY
        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        screen.blit(font.render(tool, True, BLACK), (x + 4, 12))
        x += 62

    x = 10
    for color in COLORS:
        rect = pygame.Rect(x, 36, 20, 20)
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, WHITE, rect, 2)
        else:
            pygame.draw.rect(screen, BLACK, rect, 1)
        x += 24

    screen.blit(font.render(f"Size: {brush_size} [+/-]  |  C - Clear",
                            True, WHITE), (260, 40))

    pygame.draw.rect(screen, current_color, (WIDTH - 40, 10, 25, 25))
    pygame.draw.rect(screen, WHITE, (WIDTH - 40, 10, 25, 25), 1)


def tool_at(pos):
    x = 10
    for tool in TOOLS:
        rect = pygame.Rect(x, 8, 58, 22)
        if rect.collidepoint(pos):
            return tool
        x += 62
    return None


def color_at(pos):
    x = 10
    for color in COLORS:
        rect = pygame.Rect(x, 36, 20, 20)
        if rect.collidepoint(pos):
            return color
        x += 24
    return None


def canvas_pos(pos):
    return (pos[0], pos[1] - CANVAS_Y)


def run():
    global current_color, current_tool, brush_size, drawing, start_pos

    clock = pygame.time.Clock()
    prev_pos = None
    snapshot = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    canvas.fill(WHITE)
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    brush_size = min(brush_size + 1, 30)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    brush_size = max(brush_size - 1, 1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < TOOLBAR_H:
                    t = tool_at(event.pos)
                    if t:
                        current_tool = t
                    c = color_at(event.pos)
                    if c:
                        current_color = c
                else:
                    drawing = True
                    start_pos = canvas_pos(event.pos)
                    prev_pos = start_pos
                    if current_tool in SHAPE_TOOLS:
                        snapshot = canvas.copy()

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    cp = canvas_pos(event.pos)
                    if current_tool in SHAPE_TOOLS:
                        draw_shape(canvas, current_tool, current_color,
                                   start_pos, cp, brush_size)
                    drawing = False
                    start_pos = None
                    prev_pos = None
                    snapshot = None

            elif event.type == pygame.MOUSEMOTION:
                if drawing and event.pos[1] >= CANVAS_Y:
                    cp = canvas_pos(event.pos)
                    if current_tool == TOOL_PEN:
                        if prev_pos:
                            pygame.draw.line(canvas, current_color, prev_pos, cp, brush_size)
                        prev_pos = cp
                    elif current_tool == TOOL_ERASER:
                        if prev_pos:
                            pygame.draw.line(canvas, WHITE, prev_pos, cp, brush_size * 3)
                        prev_pos = cp

        screen.fill(DARK_GRAY)

        # live preview for shapes - we draw on a copy so canvas stays clean
        if drawing and snapshot and current_tool in SHAPE_TOOLS:
            temp = snapshot.copy()
            cp = canvas_pos(pygame.mouse.get_pos())
            draw_shape(temp, current_tool, current_color, start_pos, cp, brush_size)
            screen.blit(temp, (0, CANVAS_Y))
        else:
            screen.blit(canvas, (0, CANVAS_Y))

        draw_toolbar()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    run()
