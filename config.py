SPEED = 20

COLUMNS = 10
VISIBLE_ROWS = 20
GRID_ROWS = 40
HIDDEN_ROWS = GRID_ROWS - VISIBLE_ROWS
PIECE_SPAWN_ROW_LOCATION = HIDDEN_ROWS - 3
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750

TOP_LEFT_X_COORDINATE = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y_COORDINATE = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

BOARD_END_X_COORDINATE = TOP_LEFT_X_COORDINATE + (PLAY_WIDTH)

UPCOMING_PIECES_SCREEN_LEFT_X_COORDINATE = BOARD_END_X_COORDINATE + 10
UPCOMING_PIECES_SCREEN_TOP_Y_COORDINATE = TOP_LEFT_Y_COORDINATE 
UPCOMING_PIECES_SCREEN_WIDTH = BLOCK_SIZE * COLUMNS / 2
UPCOMING_PIECES_SCREEN_HEIGHT = VISIBLE_ROWS * BLOCK_SIZE * 4 / 5

HOLD_PIECE_SCREEN_WIDTH = BLOCK_SIZE * COLUMNS / 2
HOLD_PIECE_SCREEN_HEIGHT = VISIBLE_ROWS * BLOCK_SIZE / 5
HOLD_PIECE_SCREEN_LEFT_X_COORDINATE = TOP_LEFT_X_COORDINATE - 10 - HOLD_PIECE_SCREEN_WIDTH
HOLD_PIECE_SCREEN_TOP_Y_COORDINATE = TOP_LEFT_Y_COORDINATE


# Controls
DAS_DELAY = 0.1

# SRS Kick Tables

# I Table
# Use https://tetris.wiki/File:TETR.IO_SRS%2Bkicks.png to update the table
I_PIECE_CLOCKWISE_KICK_TABLE = [
    [(1, 0), (-2, 0), (1, 2), (-2, -1)], # 3 -> 0
    [(-2, 0), (1, 0), (-2, 1), (1, -2)], # 0 -> 1
    [(-1, 0), (2, 0), (-1, -2), (2, 1)], # 1 -> 2
    [(2, 0), (-1, 0), (2, -1), (-1, 2)], # 2 -> 3
]

I_PIECE_COUNTER_CLOCKWISE_KICK_TABLE = [
    [(2, 0), (-1, 0), (2, -1), (-1, 2)], # 1 -> 0
    [(1, 0), (-2, 0), (1, 2), (-2, -1)], # 2 -> 1
    [(-2, 0), (1, 0), (-2, 1), (1, -2)], # 3 -> 2
    [(-1, 0), (2, 0), (-1, -2), (2, 1)], # 0 -> 3
]

OTHER_PIECES_CLOCKWISE_KICK_TABLE = [
    [(-1, 0), (-1, 1), (0, -2), (-1, -2)], # 3 -> 0
    [(-1, 0), (-1, -1), (0, 2), (-1, 2)], # 0 -> 1
    [(1, 0), (1, 1), (0, -2), (1, -2)], # 1 -> 2
    [(1, 0), (1, -1), (0, 2), (1, 2)], # 2 -> 3
]

OTHER_PIECES_COUNTER_CLOCKWISE_KICK_TABLE = [
    [(1, 0), (1, 1), (0, -2), (1, -2)], # 1 -> 0
    [(-1, 0), (-1, -1), (0, 2), (-1, 2)], # 2 -> 1
    [(-1, 0), (-1, 1), (0, -2), (-1, -2)], # 3 -> 2
    [(1, 0), (1, -1), (0, 2), (1, 2)], # 0 -> 3
]

TETRIO_180_KICK_TABLE = [
    [(0, 1), (-1, 1), (1, 1), (-1, 0), (1, 0)], # 2 -> 0
    [(-1, 0), (-1, -2), (-1, -1), (0, -2), (0, -1)], # 3 -> 1
    [(0,1), (1, -1), (-1, -1), (1, 0), (-1, 0)], # 0 -> 2
    [(1,0), (1, -2), (1, -1), (0, -2), (0, -1)]  # 1 -> 3
]