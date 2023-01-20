from enum import Enum

WIN_HEIGHT = 600
WIN_WIDTH = 600
FIELD_SIZE = WIN_HEIGHT / 8
NUM_OF_COLUMNS = 8
NUM_OF_ROWS = 8
MAX_FPS = 15
BEIGE = (240, 217, 181)
BROWN = (139, 69, 19)
LIGHT_BROWN = (193, 154, 107)
PIECE_PADDING = 15
GREEN = (50, 205, 50)
TITLE_RECT_MID_X = 300
TITLE_RECT_MID_Y = 180
BUTTON_OUTLINE_WIDTH = 280
BUTTON_OUTLINE_HEIGHT = 55
SLEEP_TIME_IN_PVB_GAME = 0.25
SLEEP_TIME_IN_BVB_GAME = 1.2
MINIMAX_DEPTH = 8
MAX_MOVES_WITHOUT_ATTACKS = 50


class Color(Enum):
    WHITE = 1
    BLACK = 2


class Placeholder(Enum):
    SCREEN = 1
    PIECE = 2
