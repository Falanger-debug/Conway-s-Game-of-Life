import pygame
import sys
import numpy as np

# Game settings
WIDTH, HEIGHT = 45, 45
CELL_SIZE = 10
SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE + 50  # Dodatkowy pasek na przyciski
FPS = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (0, 0, 255)
BUTTON_HOVER_COLOR = (0, 0, 200)
GRID_COLOR = (212, 201, 171)
BACKGROUND_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Grid data
grid = np.zeros((WIDTH, HEIGHT), dtype=int)
running = False  # Czy symulacja jest uruchomiona

# Draw functions
def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if grid[x, y] == 1:
                pygame.draw.rect(screen, WHITE, rect)

def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    current_color = hover_color if button_rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, current_color, button_rect)
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

# Game logic
def update_grid():
    global grid
    new_grid = np.copy(grid)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            neighbors = np.sum(grid[x-1:x+2, y-1:y+2]) - grid[x, y]
            if grid[x, y] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[x, y] = 0
            elif grid[x, y] == 0 and neighbors == 3:
                new_grid[x, y] = 1
    grid = new_grid

# Toggle cell state on click
def set_cell(x, y, state):
    grid[x, y] = state

# Load data from file
def load_data(filename="data_points/simple_example.csv"):
    global grid
    try:
        with open(filename, "r") as f:
            for line in f:
                x, y = map(int, line.strip().split(","))
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    grid[x, y] = 1
        print("Data loaded successfully")
    except FileNotFoundError:
        print("File not found")
    except ValueError:
        print("Invalid data format")

# Main loop
def main():
    global running
    while True:
        draw_grid()
        load_button = draw_button("Load", 10, SCREEN_HEIGHT - 40, 80, 30, BUTTON_COLOR, BUTTON_HOVER_COLOR)
        start_button = draw_button("Start" if not running else "Pause", 100, SCREEN_HEIGHT - 40, 80, 30, BUTTON_COLOR, BUTTON_HOVER_COLOR)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_y < SCREEN_HEIGHT - 50:  # W obszarze siatki
                    cell_x, cell_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                    if event.button == 1:  # Lewy przycisk myszy - ustawia komórkę na 1
                        set_cell(cell_x, cell_y, 1)
                    elif event.button == 3:  # Prawy przycisk myszy - ustawia komórkę na 0
                        set_cell(cell_x, cell_y, 0)
                elif load_button.collidepoint(event.pos):
                    load_data()
                elif start_button.collidepoint(event.pos):
                    running = not running

        if running:
            update_grid()

if __name__ == "__main__":
    main()
