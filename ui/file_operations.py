from app import grid, GameOfLifeApp, WIDTH, HEIGHT
from tkinter import filedialog
from settings import INITIAL_DIR

def load_data_from_file(app):
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
    GameOfLifeApp.draw_grid(app)