import pygame
import numpy as np
import time
from Models.Shapes import SHAPES, SHAPE_COLORS
from Models.Colors import BLACK, WHITE
from config import *
import random
from collections import deque

pygame.init()
# font = pygame.font.Font('arial.ttf', 25)

class Piece(object):
    def __init__(self, col: int, row: int, shapeIdx: int):
        self.col = col
        self.row = row

        self.shape = SHAPES[shapeIdx]
        self.color = SHAPE_COLORS[shapeIdx]
        self.rotation = 0 # This will be in [0, 3], for four different rotated shapes
        self.rotatedPiece = self.shape[self.rotation]
        self.width = len(self.rotatedPiece[0])
        self.height = len(self.rotatedPiece)

        self.rightCol = self.col + self.width
        self.bottomRow = self.row + self.height





class TetrisGame:

    def __init__(self):
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.key_down_time = None
        self.shifted = False
        self.reset()

    def reset(self):
        # initialize game state
        self.display.fill(BLACK)
        self.gameBoard = [[(len(SHAPE_COLORS) - 1) for _ in range(40)] for _ in range(10)]
        self.pieces = deque()
        self._add_pieces()
        self._add_new_falling_piece()
        self._draw_grid()
        self._draw_upcoming_pieces()
        self._draw_hold_piece()

    def _add_new_falling_piece(self):
        fallingPieceIdx = self.pieces.popleft()

        # Make sure there are enough pieces to fill the upcoming piece area
        if len(self.pieces) <= 6:
            self._add_pieces()

        # intialize the piece
        self.fallingPiece = Piece((COLUMNS - len(SHAPES[fallingPieceIdx][0])) // 2, -3, fallingPieceIdx)
        
        # update the game board
        self._draw_falling_piece()

    def _add_pieces(self):
        pieces = list(range(7))
        random.shuffle(pieces)
        for piece in pieces: 
            self.pieces.append(piece)

    def _draw_grid(self):
        for x in range(COLUMNS):
            for y in range(VISIBLE_ROWS):
                shiftedX = (x * BLOCK_SIZE) + TOP_LEFT_X_COORDINATE
                shiftedY = (y * BLOCK_SIZE) + TOP_LEFT_Y_COORDINATE
                boardSquare = pygame.Rect(shiftedX, shiftedY, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.display, SHAPE_COLORS[self.gameBoard[x][HIDDEN_ROWS + y]], boardSquare)

        pygame.display.flip()

    def _draw_upcoming_pieces(self):
        upcomingPiecesDisplayArea = pygame.Rect(
            UPCOMING_PIECES_SCREEN_LEFT_X_COORDINATE, 
            UPCOMING_PIECES_SCREEN_TOP_Y_COORDINATE, 
            UPCOMING_PIECES_SCREEN_WIDTH,
            UPCOMING_PIECES_SCREEN_HEIGHT)
        
        pygame.draw.rect(self.display, WHITE, upcomingPiecesDisplayArea)

        pygame.display.flip()

    def _draw_hold_piece(self):
        holdPieceDisplayArea = pygame.Rect(
            HOLD_PIECE_SCREEN_LEFT_X_COORDINATE,
            HOLD_PIECE_SCREEN_TOP_Y_COORDINATE,
            HOLD_PIECE_SCREEN_WIDTH,
            HOLD_PIECE_SCREEN_HEIGHT
        )

        pygame.draw.rect(self.display, WHITE, holdPieceDisplayArea)

        pygame.display.flip()

    def _draw_falling_piece(self):
        for col in range(self.fallingPiece.width):
            for row in range(self.fallingPiece.height):
                P = self.fallingPiece
                if P.rotatedPiece[row][col] == '0':
                    pieceColumn = P.col + col
                    pieceRow = P.row + row
                    pieceLeftXCoordinate = TOP_LEFT_X_COORDINATE + (pieceColumn * BLOCK_SIZE) 
                    pieceTopYCoordinate = TOP_LEFT_Y_COORDINATE + (pieceRow * BLOCK_SIZE)

                    fallingPieceSquare = pygame.Rect(
                        pieceLeftXCoordinate,
                        pieceTopYCoordinate,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    )

                    pygame.draw.rect(self.display, P.color, fallingPieceSquare)

        pygame.display.flip()

    def _update_ui(self):
        pass

    def play_step(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        print("going left")
                        self.key_down_time = time.time()
                        self.shifted = False
                    case pygame.K_RIGHT:
                        print("going right")
                        self.key_down_time = time.time()
                        self.shifted = False
                    case pygame.K_UP:
                        self._add_new_falling_piece()
                    case pygame.K_DOWN:
                        pass
                    case _:
                        continue

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.key_down_time = None

        # Handle DAS
        if self.key_down_time is not None and not self.shifted:
            if time.time() - self.key_down_time > DAS_DELAY:
                if keys[pygame.K_LEFT]:
                    print("DAS-ing left")
                elif keys[pygame.K_RIGHT]:
                    print("DAS-ing right")
                self.shifted = True
                self.key_down_time = None

if __name__ == '__main__':
    game = TetrisGame()
    
    # game loop
    while True:
        
        game.play_step()
        
        # if game_over == True:
            # break
        
    pygame.quit()
