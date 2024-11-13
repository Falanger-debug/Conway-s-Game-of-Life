import tkinter as tk
from datetime import time
import time
from tkinter import ttk, filedialog
import numpy as np
import settings
from settings import *

# Grid data
grid = np.zeros((WIDTH, HEIGHT), dtype=int)
active_cells = set()
running = False
fps = settings.FPS

def save_data_to_file():
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


def count_neighbors(x, y):
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


def update_grid():
    global grid, active_cells
    new_grid = np.copy(grid)
    new_active_cells = set()
    to_check = active_cells.copy()

    for (x, y) in active_cells:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    new_x, new_y = x + i, y + j
                    if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
                        to_check.add((new_x, new_y))

    for (x, y) in to_check:
        neighbors = count_neighbors(x, y)

        if grid[x, y] == 1:
            if neighbors not in settings.RULE["S"]:
                new_grid[x, y] = 0
            else:
                new_active_cells.add((x, y))
        else:
            if neighbors in settings.RULE["B"]:
                new_grid[x, y] = 1
                new_active_cells.add((x, y))

    grid = new_grid
    active_cells = new_active_cells


class GameOfLifeApp:
    def __init__(self, main_root):
        self.root = main_root  # main container for all the widgets
        self.root.title("Conway's Game of Life")
        self.root.attributes("-fullscreen", True) if FULLSCREEN else self.root.geometry("1080x720")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Apply ttk style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=BACKGROUND_COLOR)
        style.configure("TLabel", background=BACKGROUND_COLOR, foreground="white")
        style.configure("TButton", background=BUTTON_COLOR, foreground="white", font=('Helvetica', 10, 'bold'))
        style.map("TButton", background=[("active", BUTTON_HOVER_COLOR)])
        # Zoom level
        self.cell_size = CELL_SIZE
        self.offset_x = 0
        self.offset_y = 0
        self.panning = False
        self.game_loop_id = None

        self.canvas = tk.Canvas(
            main_root, bg=BACKGROUND_COLOR, highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, columnspan=5, padx=10, pady=10,
                         sticky="nsew")
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)
        self.canvas.bind("<ButtonRelease-1>", self.end_pan)
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)
        self.canvas.bind("<MouseWheel>", self.zoom)

        self.last_mouse_x = None
        self.last_mouse_y = None

        # Control panel
        control_frame = ttk.LabelFrame(main_root, text="Controls", padding=(10, 10))
        control_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Configure row and column weights to make them expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        # Buttons
        self.start_button = ttk.Button(control_frame, text="Start", command=self.toggle_running)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.clear_button = ttk.Button(control_frame, text="Clear", command=self.clear_grid)
        self.clear_button.grid(row=0, column=1, padx=5, pady=5)

        self.load_button = ttk.Button(control_frame, text="Load", command=self.load_data_from_file)
        self.load_button.grid(row=0, column=2, padx=5, pady=5)

        self.save_button = ttk.Button(control_frame, text="Save", command=save_data_to_file)
        self.save_button.grid(row=0, column=3, padx=5, pady=5)

        self.rule_label = ttk.Label(control_frame, text="Rule:")
        self.rule_label.grid(row=0, column=4, padx=5, pady=5)

        self.rule_combobox = ttk.Combobox(control_frame, values=[rule["name"] for rule in settings.RULES])
        self.rule_combobox.current(0)
        self.rule_combobox.grid(row=0, column=5, padx=5, pady=5)
        self.rule_combobox.bind("<<ComboboxSelected>>", self.change_rule)

        # FPS Selection
        self.fps_label = ttk.Label(control_frame, text="FPS:")
        self.fps_label.grid(row=0, column=6, padx=5, pady=5)

        self.fps_combobox = ttk.Combobox(control_frame, values=["5", "10", "15", "20", "30", "60", "100"])
        self.fps_combobox.set(FPS)
        self.fps_combobox.grid(row=0, column=7, padx=5, pady=5)
        self.fps_combobox.bind("<<ComboboxSelected>>", self.change_fps)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Game loop
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
                            active_cells.add((x, y))
                print("Data loaded successfully from:", file_path)
            except FileNotFoundError:
                print("File not found")
            except ValueError:
                print("Invalid data format")
        self.draw_grid()

    def game_loop(self):
        if running:
            update_grid()
        self.draw_grid()

        if self.game_loop_id is not None:
            self.root.after_cancel(self.game_loop_id)

        self.root.after(1000 // fps, self.game_loop)

    def draw_grid(self):
        self.canvas.delete("all")
        global running

        for (x, y) in active_cells:
            x1 = (x * self.cell_size) + self.offset_x
            y1 = (y * self.cell_size) + self.offset_y
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            color = LIVE_CELL_COLOR if grid[x, y] == 1 else BACKGROUND_COLOR
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=GRID_COLOR, fill=color)

    def resize_canvas(self):
        self.canvas.config(width=self.root.winfo_width() - 20, height=self.root.winfo_height() - 160)
        self.draw_grid()

    def change_rule(self, _):
        selected_rule = self.rule_combobox.get()
        settings.RULE = next(rule for rule in settings.RULES if rule["name"] == selected_rule)
        self.draw_grid()

    def toggle_running(self):
        global running
        running = not running
        self.start_button.config(text="Pause" if running else "Start")

        state = "disabled" if running else "normal"
        self.load_button.config(state=state)
        self.clear_button.config(state=state)
        self.save_button.config(state=state)

        if running:
            self.root.after(1000 // FPS, self.game_loop)

    def left_click(self, event):
        x = (event.x - self.offset_x) // self.cell_size
        y = (event.y - self.offset_y) // self.cell_size
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[x, y] = 1
        self.draw_grid()

    def right_click(self, event):
        x = (event.x - self.offset_x) // self.cell_size
        y = (event.y - self.offset_y) // self.cell_size
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[x, y] = 0
        self.draw_grid()

    def zoom(self, event):
        if event.delta > 0 and self.cell_size < MAX_CELL_SIZE:
            self.cell_size += 1
        elif event.delta < 0 and self.cell_size > MIN_CELL_SIZE:
            self.cell_size -= 1
        self.draw_grid()

    def start_pan(self, event):
        self.panning = True
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def pan(self, event):
        if self.last_mouse_x is not None and self.last_mouse_y is not None:
            dx = event.x - self.last_mouse_x
            dy = event.y - self.last_mouse_y
            self.offset_x += dx
            self.offset_y += dy
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        self.draw_grid()

    def end_pan(self, _):
        self.panning = False

    def clear_grid(self):
        if running:
            return
        global grid
        grid = np.zeros((WIDTH, HEIGHT), dtype=int)
        self.draw_grid()

    def on_closing(self):
        self.root.destroy()

    def change_fps(self, _):
        global fps
        fps = int(self.fps_combobox.get())

        if running:
            self.game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameOfLifeApp(root)
    root.mainloop()
