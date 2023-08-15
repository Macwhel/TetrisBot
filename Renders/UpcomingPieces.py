# Draws the box with the 5 upcoming pieces
from Models.Colors import WHITE
from config import *
import pygame


def first_five_pieces(pieceBag):
    pieceBagAsList = list(pieceBag)
    return pieceBagAsList[:5]


def draw_upcoming_pieces(display, pieceBag):
    upcomingPiecesDisplayArea = pygame.Rect(
        UPCOMING_PIECES_SCREEN_LEFT_X_COORDINATE,
        UPCOMING_PIECES_SCREEN_TOP_Y_COORDINATE,
        UPCOMING_PIECES_SCREEN_WIDTH,
        UPCOMING_PIECES_SCREEN_HEIGHT,
    )

    rectangles = [pygame.draw.rect(display, WHITE, upcomingPiecesDisplayArea)]

    firstFivePieces = first_five_pieces(pieceBag)

    heightForEachPiece = UPCOMING_PIECES_SCREEN_HEIGHT / 5
    widthForEachPiece = UPCOMING_PIECES_SCREEN_WIDTH

    for i, piece in enumerate(firstFivePieces):
        iPieceOffset = 0
        if piece.shapeIdx == 0:
            iPieceOffset = 1
        numberOfXSections = piece.piece_width + 2  # type: ignore
        numberOfYSections = piece.piece_height + 2 + 2 * iPieceOffset  # type: ignore

        lengthOfEachXSection = widthForEachPiece / numberOfXSections
        lengthOfEachYSection = heightForEachPiece / numberOfYSections

        for col in range(piece.piece_width):
            for row in range(piece.piece_height):
                if piece.rotatedPiece[row + iPieceOffset][col] == "0":
                    holdPieceXCoord = (
                        UPCOMING_PIECES_SCREEN_LEFT_X_COORDINATE
                        + (col + 1) * lengthOfEachXSection
                    )
                    holdPieceYCoord = (
                        UPCOMING_PIECES_SCREEN_TOP_Y_COORDINATE
                        + (row + 1 + iPieceOffset) * lengthOfEachYSection
                        + i * heightForEachPiece
                    )
                    holdPieceSquare = pygame.Rect(
                        holdPieceXCoord,
                        holdPieceYCoord,
                        lengthOfEachXSection,
                        lengthOfEachYSection,
                    )

                    rectangles.append(
                        pygame.draw.rect(display, piece.color, holdPieceSquare)
                    )

    pygame.display.update(rectangles)
