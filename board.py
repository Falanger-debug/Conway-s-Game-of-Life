import tkinter as tk
from tkinter import filedialog

import numpy as np

# Game settings
WIDTH, HEIGHT = 250, 250
CELL_SIZE = 10
FPS = 1

# Default directory for file dialog
INITIAL_DIR = "./data_points"

# B: Birth, S: Survival, [Number of Neighbors]
RULES = [
    {
        "name": "GAME_OF_LIFE",
        "B": [3],
        "S": [2, 3]
    },
    {
        "name": "SEEDS",
        "B": [2],
        "S": []
    },
    {
        "name": "LIFE_WITHOUT_DEATH",
        "B": [3],
        "S": [0, 1, 2, 3, 4, 5, 6, 7, 8]
    },
    {
        "name": "CORAL",
        "B": [3],
        "S": [4, 5, 6, 7, 8]
    },
    {
        "name": "AMOEBA",
        "B": [3, 5, 7],
        "S": [1, 3, 5, 8]
    },
    {
        "name": "DAY_AND_NIGHT",
        "B": [3, 6, 7, 8],
        "S": [3, 4, 6, 7, 8]
    },
    {
        "name": "LONG_LIFE",
        "B": [3, 4, 5],
        "S": [5]
    }
]
RULE = RULES[0]

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
        self.root = root  # main container for all the widgets
        self.root.title(RULE["name"])

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

        self.save_button = tk.Button(
            root, text="Save", command=self.save_data_to_file, bg=BUTTON_COLOR, fg="white"
        )
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        self.start_button = tk.Button(
            root, text="Start", command=self.toggle_running, bg=BUTTON_COLOR, fg="white"
        )
        self.start_button.grid(row=1, column=2, padx=5, pady=5)

        self.clear_button = tk.Button(
            root, text="Clear", command=self.clear_grid, bg=BUTTON_COLOR, fg="white"
        )
        self.clear_button.grid(row=1, column=3, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Game loop
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for x in range(WIDTH):
            for y in range(HEIGHT):
                x1, y1 = x * CELL_SIZE, y * CELL_SIZE  # top left corner of the cell
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE  # bottom right corner of the cell
                color = "white" if grid[x, y] == 1 else BACKGROUND_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=GRID_COLOR, fill=color)

    def count_neighbors(self, x, y):
        neighbors = 0
        for i in range(-1, 2):
            if x + i < 0 or x + i >= WIDTH:
                continue
            for j in range(-1, 2):
                if y + j < 0 or y + j >= HEIGHT:
                    continue
                if i == 0 and j == 0:
                    continue
                neighbors += grid[x + i, y + j]
        return neighbors


    def update_grid(self):
        global grid
        new_grid = np.copy(grid)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                neighbors = self.count_neighbors(x, y)
                if grid[x, y] == 1 and (neighbors not in RULE["S"]):
                    new_grid[x, y] = 0
                elif grid[x, y] == 0 and neighbors in RULE["B"]:
                    new_grid[x, y] = 1
        grid = new_grid
        print("Grid updated")

    def game_loop(self):
        if running:
            print("Game loop running")
            self.update_grid()
        self.draw_grid()
        self.root.after(1000 // FPS, self.game_loop)

    def toggle_running(self):
        global running
        running = not running
        self.start_button.config(text="Pause" if running else "Start", bg=BUTTON_COLOR)

        state = "disabled" if running else "normal"
        self.load_button.config(state=state)
        self.clear_button.config(state=state)
        self.save_button.config(state=state)

        print(f"Game {'started' if running else 'paused'}")
        if running:
            self.root.after(1000 // FPS, self.game_loop)

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
            title="Select a file", filetypes=[("CSV files", "*.csv")], initialdir=INITIAL_DIR
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

    def save_data_to_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save as", defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")], initialdir=INITIAL_DIR
        )
        if file_path:
            try:
                with open(file_path, "w") as f:
                    for x in range(WIDTH):
                        for y in range(HEIGHT):
                            if grid[x, y] == 1:
                                f.write(f"{x},{y}\n")
                print("Data saved successfully to:", file_path)
            except FileNotFoundError:
                print("File not found")
            except Exception as e:
                print("Error saving file:", e)

    def clear_grid(self):
        if running:
            return
        global grid
        grid = np.zeros((WIDTH, HEIGHT), dtype=int)
        self.draw_grid()

    def on_closing(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameOfLifeApp(root)
    root.mainloop()
