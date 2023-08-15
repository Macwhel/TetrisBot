from Utils.FallingPiece.AddNewFallingPiece import add_new_falling_piece
from Utils.LineClears.RemoveFullRows import remove_full_rows
from config import HIDDEN_ROWS


def place_falling_piece(fallingPiece, gameBoard, display, pieceBag, callback=None):
    for col in range(fallingPiece.width):
        for row in range(fallingPiece.height):
            P = fallingPiece
            gridRow = P.row + row + HIDDEN_ROWS
            gridCol = P.col + col
            if P.rotatedPiece[row][col] == "0":
                # Please change this later. This is not readable. But basically our color is associated with the shapeIdx
                gameBoard[gridRow, gridCol] = P.shapeIdx
    gameBoard = remove_full_rows(gameBoard)

    if callback:
        callback()

    return (add_new_falling_piece(display, pieceBag), gameBoard)
