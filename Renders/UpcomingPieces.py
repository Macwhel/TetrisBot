# Draws the box with the 5 upcoming pieces
from Models.Colors import WHITE
from config import *
import pygame


def draw_upcoming_pieces(display):
    upcomingPiecesDisplayArea = pygame.Rect(
        UPCOMING_PIECES_SCREEN_LEFT_X_COORDINATE,
        UPCOMING_PIECES_SCREEN_TOP_Y_COORDINATE,
        UPCOMING_PIECES_SCREEN_WIDTH,
        UPCOMING_PIECES_SCREEN_HEIGHT,
    )

    rectangles = [pygame.draw.rect(display, WHITE, upcomingPiecesDisplayArea)]

    pygame.display.update(rectangles)
