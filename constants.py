# Dimensions of the game board (standard Connect 4 size: 7 columns x 6 rows)
BOARD_WIDTH = 7
BOARD_HEIGHT = 6

# Constants to represent the contents of a board cell
EMPTY = 0          # An empty cell
PLAYER_PIECE = 1   # A cell occupied by the player's piece
AI_PIECE = 2       # A cell occupied by the AI's piece

# Number of pieces in a row needed to win the game
WINDOW_LENGTH = 4

# Size of each square on the screen (for rendering)
SQUARE_SIZE = 100

# Radius of the game piece (circle), slightly smaller than half the square to leave margin
RADIUS = int(SQUARE_SIZE / 2 - 5)

# Width and height of the game window in pixels
WIDTH = BOARD_WIDTH * SQUARE_SIZE                     # Total width based on number of columns
HEIGHT = (BOARD_HEIGHT + 1) * SQUARE_SIZE             # Extra row added at top for drop area or UI

# RGB color definitions for rendering elements
BLUE = (0, 0, 255)        # Board background color
BLACK = (0, 0, 0)         # Background or empty space color
RED = (255, 0, 0)         # Player's piece color
YELLOW = (255, 255, 0)    # AI's piece color
WHITE = (255, 255, 255)   # Optional: used for text or other UI elements
