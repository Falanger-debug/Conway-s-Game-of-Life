import pygame
import sys
import numpy as np

# Game settings
WIDTH = 45
HEIGHT = 45
CELL_SIZE = 10
SCREEN_WIDTH = WIDTH * CELL_SIZE
HEIGHT_WIDTH = HEIGHT * CELL_SIZE
FPS = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (212, 201, 171)
BUTTON_COLOR = (0, 0, 255)
BUTTON_HOVER_COLOR = (0, 0, 200)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT_WIDTH))
pygame.display.set_caption("Conway's Game of Life")


# Create the grid
def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT_WIDTH, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    return button_rect


def load_data():
    print("Loading data...")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_grid()
    load_button = draw_button("Load", 10, SCREEN_WIDTH - 40, 80, 30, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    start_button = draw_button("Start", 100, SCREEN_WIDTH - 40, 80, 30, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    pygame.display.flip()  # Update the display
