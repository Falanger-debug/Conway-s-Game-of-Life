import tkinter as tk
from tkinter import filedialog
import numpy as np

# Game settings
WIDTH, HEIGHT = 60, 60
CELL_SIZE = 10
FPS = 10

# Colors
BUTTON_COLOR = "blue"
BUTTON_HOVER_COLOR = "dark blue"
GRID_COLOR = "#D4C9AB"
BACKGROUND_COLOR = "black"

# Grid data
grid = np.zeros((WIDTH, HEIGHT), dtype=int)
running = False


class GameOfLifeApp:
    def __init__(self, root):
        self.root = root # main container for all the widgets
        self.root.title("Conway's Game of Life")

        self.canvas = tk.Canvas(
            root, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, bg=BACKGROUND_COLOR
        )
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

        # Buttons
        self.load_button = tk.Button(
            root, text="Load", command=self.load_data_from_file, bg=BUTTON_COLOR, fg="white"
        )
        self.load_button.grid(row=1, column=0, padx=5, pady=5)

        self.start_button = tk.Button(
            root, text="Start", command=self.toggle_running, bg=BUTTON_COLOR, fg="white"
        )
        self.start_button.grid(row=1, column=1, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Game loop
        self.draw_grid()
        self.root.after(1000 // FPS, self.game_loop)

    def draw_grid(self):
        self.canvas.delete("all")
        for x in range(WIDTH):
            for y in range(HEIGHT):
                x1, y1 = x * CELL_SIZE, y * CELL_SIZE # top left corner of the cell
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE # bottom right corner of the cell
                color = "white" if grid[x, y] == 1 else BACKGROUND_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=GRID_COLOR, fill=color)

    def update_grid(self):
        global grid
        new_grid = np.copy(grid)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                neighbors = np.sum(grid[x - 1 : x + 2, y - 1 : y + 2]) - grid[x, y]
                if grid[x, y] == 1 and (neighbors < 2 or neighbors > 3):
                    new_grid[x, y] = 0
                elif grid[x, y] == 0 and neighbors == 3:
                    new_grid[x, y] = 1
        grid = new_grid

    def game_loop(self):
        if running:
            self.update_grid()
        self.draw_grid()
        self.root.after(1000 // FPS, self.game_loop)

    def toggle_running(self):
        global running
        running = not running
        self.start_button.config(text="Pause" if running else "Start")

    def left_click(self, event):
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[x, y] = 1
        self.draw_grid()

    def right_click(self, event):
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[x, y] = 0
        self.draw_grid()

    def load_data_from_file(self):
        global grid
        file_path = filedialog.askopenfilename(
            title="Select a file", filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                with open(file_path, "r") as f:
                    for line in f:
                        x, y = map(int, line.strip().split(","))
                        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                            grid[x, y] = 1
                print("Data loaded successfully from:", file_path)
            except FileNotFoundError:
                print("File not found")
            except ValueError:
                print("Invalid data format")
        self.draw_grid()

    def on_closing(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameOfLifeApp(root)
    root.mainloop()
