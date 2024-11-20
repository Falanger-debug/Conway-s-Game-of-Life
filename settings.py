# Game settings
WIDTH, HEIGHT = 150, 100
CELL_SIZE = 10
MIN_CELL_SIZE = 2
MAX_CELL_SIZE = 50
FPS = 15
FULLSCREEN = False

# Default directory for file dialog
INITIAL_DIR = "./data_points"

# B: Birth, S: Survival, [Number of Neighbors]
RULES = [
    {"name": "GAME_OF_LIFE","B": [3],"S": [2, 3]},
    {"name": "SEEDS","B": [2],"S": []},
    {"name": "LIFE_WITHOUT_DEATH","B": [3],"S": [0, 1, 2, 3, 4, 5, 6, 7, 8]},
    {"name": "CORAL","B": [3],"S": [4, 5, 6, 7, 8]},
    {"name": "AMOEBA","B": [3, 5, 7],"S": [1, 3, 5, 8]},
    {"name": "DAY_AND_NIGHT","B": [3, 6, 7, 8],"S": [3, 4, 6, 7, 8]},
    {"name": "LONG_LIFE","B": [3, 4, 5],"S": [5]}
]
RULE = RULES[0]

# Colors
BUTTON_COLOR = "#6272a4"
BUTTON_HOVER_COLOR = "#bd93f9"
GRID_COLOR = "#44475a"
LIVE_CELL_COLOR = "#50fa7b"
BACKGROUND_COLOR = "#282a36"