from enum import Enum
from Utils.FallingPiece.MoveFallingPiece import move_piece

from config import COLUMNS


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


def DAS(fallingPiece, gameBoard, direction: Direction):
    for _ in range(COLUMNS):
        move_piece(fallingPiece, gameBoard, direction.value, 0)
