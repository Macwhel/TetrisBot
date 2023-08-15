# Add the new piece at game start and when another piece is placed
from Models.Piece import Piece
from Models.Shapes import SHAPES
from Renders.Grid import draw_falling_piece
from Renders.UpcomingPieces import draw_upcoming_pieces
from Utils.PieceBag.AddPiecesToBag import add_pieces_to_bag
from config import COLUMNS, PIECE_SPAWN_HEIGHT_OFFSET


def add_new_falling_piece(display, pieceBag):
    # intialize the piece
    fallingPiece = pieceBag.popleft()

    # Make sure there are enough pieces to fill the upcoming piece area
    if len(pieceBag) <= 6:
        add_pieces_to_bag(pieceBag)

    # update the game board
    draw_falling_piece(display, fallingPiece)

    draw_upcoming_pieces(display, pieceBag)

    return fallingPiece, False
