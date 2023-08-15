# Add pieces to the piece bag
# We're using a 7 bag randomizer or w/e it's called
import random
from Models.Piece import Piece
from Models.Shapes import SHAPES

from config import COLUMNS, PIECE_SPAWN_HEIGHT_OFFSET


def add_pieces_to_bag(piece_bag):
    pieceIdxs = list(range(7))
    random.shuffle(pieceIdxs)
    for pieceIdx in pieceIdxs:
        piece_bag.append(
            Piece(
                (COLUMNS - len(SHAPES[pieceIdx][0])) // 2,
                PIECE_SPAWN_HEIGHT_OFFSET,
                pieceIdx,
            )
        )
