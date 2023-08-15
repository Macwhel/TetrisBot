from config import *
import pygame
from Models.Shapes import *


# In charge of drawing the falling piece
def draw_falling_piece(display, fallingPiece):
    rectangles = []
    for col in range(fallingPiece.width):
        for row in range(fallingPiece.height):
            if fallingPiece.rotatedPiece[row][col] == "0":
                pieceColumn = fallingPiece.col + col
                pieceRow = fallingPiece.row + row
                pieceLeftXCoordinate = TOP_LEFT_X_COORDINATE + (
                    pieceColumn * BLOCK_SIZE
                )
                pieceTopYCoordinate = TOP_LEFT_Y_COORDINATE + (pieceRow * BLOCK_SIZE)

                fallingPieceSquare = pygame.Rect(
                    pieceLeftXCoordinate,
                    pieceTopYCoordinate,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )

                rectangles.append(
                    pygame.draw.rect(display, fallingPiece.color, fallingPieceSquare)
                )

    pygame.display.update(rectangles)


def draw_rows_above_grid(display, gameBoard):
    rectangles = []
    for x in range(COLUMNS):
        for y in range(COLUMNS_ABOVE_GRID):
            shiftedX = (x * BLOCK_SIZE) + TOP_LEFT_X_COORDINATE
            shiftedY = ((y - 3) * BLOCK_SIZE) + TOP_LEFT_Y_COORDINATE
            boardTile = pygame.Rect(shiftedX, shiftedY, BLOCK_SIZE, BLOCK_SIZE)
            rectangles.append(pygame.draw.rect(display, BLACK, boardTile))
    return rectangles


def draw_grid(display, gameBoard):
    rectangles = draw_rows_above_grid(display, gameBoard)
    for x in range(COLUMNS):
        for y in range(VISIBLE_ROWS):
            shiftedX = (x * BLOCK_SIZE) + TOP_LEFT_X_COORDINATE
            shiftedY = (y * BLOCK_SIZE) + TOP_LEFT_Y_COORDINATE
            boardSquare = pygame.Rect(shiftedX, shiftedY, BLOCK_SIZE, BLOCK_SIZE)
            rectangles.append(
                pygame.draw.rect(
                    display, SHAPE_COLORS[gameBoard[HIDDEN_ROWS + y, x]], boardSquare
                )
            )

    pygame.display.update(rectangles)
