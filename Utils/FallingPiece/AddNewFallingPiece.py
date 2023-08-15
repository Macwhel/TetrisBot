# Add the new piece at game start and when another piece is placed
from Models.Piece import Piece
from Models.Shapes import SHAPES
from Renders.Grid import draw_falling_piece
from Utils.PieceBag.AddPiecesToBag import add_pieces_to_bag
from config import COLUMNS, PIECE_SPAWN_HEIGHT_OFFSET


def add_new_falling_piece(display, piece_bag):
    fallingPieceIdx = piece_bag.popleft()

    # Make sure there are enough pieces to fill the upcoming piece area
    if len(piece_bag) <= 6:
        add_pieces_to_bag(piece_bag)

    # intialize the piece
    fallingPiece = Piece(
        (COLUMNS - len(SHAPES[fallingPieceIdx][0])) // 2,
        PIECE_SPAWN_HEIGHT_OFFSET,
        fallingPieceIdx,
    )

    # update the game board
    draw_falling_piece(display, fallingPiece)

    return fallingPiece, False
