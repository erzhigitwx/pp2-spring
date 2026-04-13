import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
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

font = pygame.font.SysFont('Arial', 14)

COLORS = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, WHITE]

TOOL_PEN = 'pen'
TOOL_RECT = 'rect'
TOOL_CIRCLE = 'circle'
TOOL_ERASER = 'eraser'
TOOLS = [TOOL_PEN, TOOL_RECT, TOOL_CIRCLE, TOOL_ERASER]

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill(WHITE)

current_color = BLACK
current_tool = TOOL_PEN
brush_size = 3
drawing = False
start_pos = None


def draw_toolbar():
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, TOOLBAR_H))

    x = 10
    for tool in TOOLS:
        rect = pygame.Rect(x, 8, 60, 20)
        active = tool == current_tool
        bg = WHITE if active else GRAY
        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        label = font.render(tool.capitalize(), True, BLACK)
        screen.blit(label, (x + 5, 11))
        x += 68

    x = 300
    for color in COLORS:
        rect = pygame.Rect(x, 8, 22, 22)
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, WHITE, rect, 2)
        else:
            pygame.draw.rect(screen, BLACK, rect, 1)
        x += 28

    size_text = font.render(f"Size: {brush_size}", True, WHITE)
    screen.blit(size_text, (10, 36))
    screen.blit(font.render("[+/-]", True, GRAY), (80, 36))

    screen.blit(font.render("C - Clear", True, GRAY), (160, 36))

    pygame.draw.rect(screen, current_color, (WIDTH - 40, 10, 25, 25))
    pygame.draw.rect(screen, WHITE, (WIDTH - 40, 10, 25, 25), 1)


def get_tool_at(pos):
    x = 10
    for tool in TOOLS:
        rect = pygame.Rect(x, 8, 60, 20)
        if rect.collidepoint(pos):
            return tool
        x += 68
    return None


def get_color_at(pos):
    x = 300
    for color in COLORS:
        rect = pygame.Rect(x, 8, 22, 22)
        if rect.collidepoint(pos):
            return color
        x += 28
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
                    tool = get_tool_at(event.pos)
                    if tool:
                        current_tool = tool
                    color = get_color_at(event.pos)
                    if color:
                        current_color = color
                else:
                    drawing = True
                    start_pos = canvas_pos(event.pos)
                    prev_pos = start_pos
                    if current_tool in (TOOL_RECT, TOOL_CIRCLE):
                        snapshot = canvas.copy()

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    cp = canvas_pos(event.pos)
                    if current_tool == TOOL_RECT:
                        x = min(start_pos[0], cp[0])
                        y = min(start_pos[1], cp[1])
                        w = abs(cp[0] - start_pos[0])
                        h = abs(cp[1] - start_pos[1])
                        pygame.draw.rect(canvas, current_color, (x, y, w, h), brush_size)
                    elif current_tool == TOOL_CIRCLE:
                        cx = (start_pos[0] + cp[0]) // 2
                        cy = (start_pos[1] + cp[1]) // 2
                        rx = abs(cp[0] - start_pos[0]) // 2
                        ry = abs(cp[1] - start_pos[1]) // 2
                        r = max(rx, ry)
                        if r > 0:
                            pygame.draw.circle(canvas, current_color, (cx, cy), r, brush_size)
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

        if drawing and snapshot and current_tool in (TOOL_RECT, TOOL_CIRCLE):
            temp = snapshot.copy()
            cp = canvas_pos(pygame.mouse.get_pos())
            if current_tool == TOOL_RECT:
                x = min(start_pos[0], cp[0])
                y = min(start_pos[1], cp[1])
                w = abs(cp[0] - start_pos[0])
                h = abs(cp[1] - start_pos[1])
                pygame.draw.rect(temp, current_color, (x, y, w, h), brush_size)
            elif current_tool == TOOL_CIRCLE:
                cx = (start_pos[0] + cp[0]) // 2
                cy = (start_pos[1] + cp[1]) // 2
                r = max(abs(cp[0] - start_pos[0]), abs(cp[1] - start_pos[1])) // 2
                if r > 0:
                    pygame.draw.circle(temp, current_color, (cx, cy), r, brush_size)
            screen.blit(temp, (0, CANVAS_Y))
        else:
            screen.blit(canvas, (0, CANVAS_Y))

        draw_toolbar()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    run()
