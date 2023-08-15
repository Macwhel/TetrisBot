from Utils.FallingPiece.MoveFallingPiece import move_piece
from Utils.FallingPiece.PlaceFallingPiece import place_falling_piece
from config import PIECE_SPAWN_HEIGHT_OFFSET, VISIBLE_ROWS


def move_piece_to_bottom(piece, gameBoard):
    for _ in range(VISIBLE_ROWS - PIECE_SPAWN_HEIGHT_OFFSET):
        move_piece(piece, gameBoard, 0, 1)


def hard_drop(fallingPiece, gameBoard, display, pieceBag):
    move_piece_to_bottom(fallingPiece, gameBoard)
    return place_falling_piece(fallingPiece, gameBoard, display, pieceBag)


def soft_drop(fallingPiece, gameBoard):
    move_piece_to_bottom(fallingPiece, gameBoard)
