# Add pieces to the piece bag
# We're using a 7 bag randomizer or w/e it's called
import random


def add_pieces_to_bag(piece_bag):
    pieces = list(range(7))
    random.shuffle(pieces)
    for piece in pieces:
        piece_bag.append(piece)
