from typing import List
from Models.Piece import Piece
from Models.Rotations import Rotations
from Utils.FallingPiece.IsFallingPieceLegal import is_falling_piece_legal
from config import (
    I_PIECE_CLOCKWISE_KICK_TABLE,
    I_PIECE_COUNTER_CLOCKWISE_KICK_TABLE,
    OTHER_PIECES_CLOCKWISE_KICK_TABLE,
    OTHER_PIECES_COUNTER_CLOCKWISE_KICK_TABLE,
    TETRIO_180_KICK_TABLE,
)


def _get_wallkick_table_row(fallingPiece, rotation) -> List[tuple]:
    rotationIndex = fallingPiece.rotation
    match rotation:
        case Rotations.CLOCKWISE:
            # This could be modularized but seems a bit unnecessary rn
            if fallingPiece.shapeIdx == 0:
                return I_PIECE_CLOCKWISE_KICK_TABLE[rotationIndex]
            else:
                return OTHER_PIECES_CLOCKWISE_KICK_TABLE[rotationIndex]
        case Rotations.COUNTER_CLOCKWISE:
            if fallingPiece.shapeIdx == 0:
                return I_PIECE_COUNTER_CLOCKWISE_KICK_TABLE[rotationIndex]
            else:
                return OTHER_PIECES_COUNTER_CLOCKWISE_KICK_TABLE[rotationIndex]
        case Rotations.ONE_EIGHTY:
            # There might be a separate one for I pieces idk
            return TETRIO_180_KICK_TABLE[rotationIndex]
        case _:
            return []  # There's a problem


def handle_wall_kicks(fallingPiece: Piece, gameBoard, rotation):
    tableRow = _get_wallkick_table_row(fallingPiece, rotation)
    initialCol = fallingPiece.col
    initialRow = fallingPiece.row
    for i in range(len(tableRow)):
        dx, dy = tableRow[i]
        fallingPiece.col = initialCol + dx
        fallingPiece.row = initialRow + dy
        if is_falling_piece_legal(fallingPiece, gameBoard):
            return True
    fallingPiece.col = initialCol
    fallingPiece.row = initialRow

    return False
