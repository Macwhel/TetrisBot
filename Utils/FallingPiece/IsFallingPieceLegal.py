from Models.Shapes import SHAPE_COLORS
from config import COLUMNS


def is_falling_piece_legal(fallingPiece, gameBoard):
    for x in range(fallingPiece.width):
        for y in range(fallingPiece.height):
            if fallingPiece.rotatedPiece[y][x] == "0":
                xCoord = fallingPiece.col + x
                yCoord = fallingPiece.row + y + 20
                if (
                    xCoord < 0
                    or xCoord >= COLUMNS
                    or yCoord >= 40
                    or gameBoard[yCoord, xCoord] != (len(SHAPE_COLORS) - 1)
                ):
                    return False

    return True
