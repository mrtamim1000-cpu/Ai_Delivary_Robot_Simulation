
# AI Delivery Robot Simulation

# Screen Settings
MAP_WIDTH = 800
SIDEBAR_WIDTH = 280
SCREEN_WIDTH = MAP_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = 600
SCREEN_TITLE = "AI Delivery Robot Simulation"

# Grid Settings
CELL_SIZE = 40

ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = MAP_WIDTH // CELL_SIZE

# Robot Starting Position
START = (1, 1)

# Delivery Destination
GOAL = (13, 18)
#blocked cells
BLOCKED = [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9)]

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)

BLUE = (40, 100, 230)
GREEN = (40, 180, 90)
RED = (230, 70, 70)
YELLOW = (255, 220, 0)

# Robot Settings
ROBOT_SPEED = 5

# Path Settings
PATH_COLOR = (100, 180, 255)
OBSTACLE_COLOR = (60, 60, 60)
