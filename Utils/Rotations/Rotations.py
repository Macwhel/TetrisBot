from Models.Rotations import Rotations
from Utils.FallingPiece.IsFallingPieceLegal import is_falling_piece_legal
from Utils.Rotations.HandleWallKicks import handle_wall_kicks


def rotate_clockwise(fallingPiece, gameBoard):
    fallingPiece.rotate_clockwise()
    if not is_falling_piece_legal(fallingPiece, gameBoard):
        # There's a separate kick table for the I piece
        if handle_wall_kicks(fallingPiece, gameBoard, Rotations.CLOCKWISE):
            return
        fallingPiece.reset_setting()


def rotate_counter_clockwise(fallingPiece, gameBoard):
    _rotate(fallingPiece, Rotations.COUNTER_CLOCKWISE)
    if not is_falling_piece_legal(fallingPiece, gameBoard):
        if handle_wall_kicks(fallingPiece, gameBoard, Rotations.COUNTER_CLOCKWISE):
            return
        fallingPiece.reset_setting()


def rotate_180(fallingPiece, gameBoard):
    _rotate(fallingPiece, Rotations.ONE_EIGHTY)
    if not is_falling_piece_legal(fallingPiece, gameBoard):
        if handle_wall_kicks(fallingPiece, gameBoard, Rotations.ONE_EIGHTY):
            return
        fallingPiece.reset_setting()


def _rotate(fallingPiece, rotation):
    fallingPiece.save_original_setting()
    match rotation:
        case Rotations.CLOCKWISE:
            fallingPiece.rotate_clockwise()
        case Rotations.COUNTER_CLOCKWISE:
            fallingPiece.rotate_counter_clockwise()
        case Rotations.ONE_EIGHTY:
            fallingPiece.rotate_180()
        case _:
            raise ValueError("This rotation doesn't exist")
