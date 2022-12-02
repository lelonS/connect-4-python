import os

# Root path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Assets path
ASSETS_PATH = os.path.join(ROOT_PATH, 'assets')

# Screen Size
WIDTH = 1280
HEIGHT = 800

# Board size
MAX_BOARD_WIDTH = int(WIDTH * 0.8)
MAX_BOARD_HEIGHT = int(HEIGHT * 0.9)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)
BG_COLOR_MAIN_MENU = (5, 10, 50)

# Player colors
BANANA = (229, 162, 17)
TART = (211, 39, 39)
PLR_COLORS = (BANANA, TART, GREEN, BLUE, WHITE)
BLIND_COLORS = ((127, 127, 127), (127, 127, 127))

# Board color
SEABLUE = (40, 60, 245)

# Variables
BOARD_BOTTOM_LEFT = (0, HEIGHT)
TILE_SIZE = 80

# Font
GAME_FONT = "RobotoMono-Regular.ttf"
FONT_PATH = os.path.join(ASSETS_PATH, GAME_FONT)
