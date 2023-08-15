import pygame
from Models.Colors import WHITE
from config import *


# Draws the box with the hold piece
def draw_hold_piece_background(display):
    holdPieceDisplayArea = pygame.Rect(
        HOLD_PIECE_SCREEN_LEFT_X_COORDINATE,
        HOLD_PIECE_SCREEN_TOP_Y_COORDINATE,
        HOLD_PIECE_SCREEN_WIDTH,
        HOLD_PIECE_SCREEN_HEIGHT,
    )

    rectangles = [pygame.draw.rect(display, WHITE, holdPieceDisplayArea)]

    pygame.display.update(rectangles)


# Draws the hold piece itself
def draw_hold_piece(display, holdPiece):
    draw_hold_piece_background(display)
    if holdPiece:
        iPieceOffset = 0
        if holdPiece.shapeIdx == 0:
            iPieceOffset = 1
        numberOfXSections = holdPiece.piece_width + 2  # type: ignore
        numberOfYSections = holdPiece.piece_height + 2 + 2 * iPieceOffset  # type: ignore

        lengthOfEachXSection = HOLD_PIECE_SCREEN_WIDTH / numberOfXSections
        lengthOfEachYSection = HOLD_PIECE_SCREEN_HEIGHT / numberOfYSections
        rectangles = []
        for col in range(holdPiece.piece_width):
            for row in range(holdPiece.piece_height):
                if holdPiece.rotatedPiece[row + iPieceOffset][col] == "0":
                    holdPieceXCoord = (
                        HOLD_PIECE_SCREEN_LEFT_X_COORDINATE
                        + (col + 1) * lengthOfEachXSection
                    )
                    holdPieceYCoord = (
                        HOLD_PIECE_SCREEN_TOP_Y_COORDINATE
                        + (row + 1 + iPieceOffset) * lengthOfEachYSection
                    )
                    holdPieceSquare = pygame.Rect(
                        holdPieceXCoord,
                        holdPieceYCoord,
                        lengthOfEachXSection,
                        lengthOfEachYSection,
                    )

                    rectangles.append(
                        pygame.draw.rect(display, holdPiece.color, holdPieceSquare)
                    )

        pygame.display.update(rectangles)
