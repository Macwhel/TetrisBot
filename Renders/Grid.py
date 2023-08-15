from config import *
import pygame
from Models.Shapes import *


def draw_columns_above_grid(display):
    rectangles = []
    for x in range(COLUMNS):
        for y in range(COLUMNS_ABOVE_GRID):
            shiftedX = (x * BLOCK_SIZE) + TOP_LEFT_X_COORDINATE
            shiftedY = ((y - 3) * BLOCK_SIZE) + TOP_LEFT_Y_COORDINATE
            boardTile = pygame.Rect(shiftedX, shiftedY, BLOCK_SIZE, BLOCK_SIZE)
            rectangles.append(pygame.draw.rect(display, BLACK, boardTile))
    return rectangles


def draw_grid(display, gameBoard):
    rectangles = draw_columns_above_grid(display)
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
