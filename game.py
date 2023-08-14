import pygame
import numpy as np
from typing import List
import time
from Models.Piece import Piece
from Models.Rotations import Rotations
from Models.Shapes import SHAPES, SHAPE_COLORS
from Models.Colors import BLACK, WHITE
from config import *
import random
from collections import deque
import pprint as pp

pygame.init()

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
        self.gameBoard = np.full((40, 10), len(SHAPE_COLORS) - 1)

        # Reset piece bag
        self.piece_bag = deque()
        self._add_pieces_to_bag()
        self._add_new_falling_piece()
        self._draw_grid()
        self._draw_upcoming_pieces()
        self._draw_hold_piece()

    # Add the new piece at game start and when another piece is placed
    def _add_new_falling_piece(self):
        fallingPieceIdx = self.piece_bag.popleft()

        # Make sure there are enough pieces to fill the upcoming piece area
        if len(self.piece_bag) <= 6:
            self._add_pieces_to_bag()

        # intialize the piece
        self.fallingPiece = Piece((COLUMNS - len(SHAPES[fallingPieceIdx][0])) // 2, PIECE_SPAWN_HEIGHT_OFFSET, fallingPieceIdx)
        
        # update the game board
        self._draw_falling_piece()

    # Add pieces to the piece bag
    # We're using a 7 bag randomizer or w/e it's called
    def _add_pieces_to_bag(self):
        pieces = list(range(7))
        random.shuffle(pieces)
        for piece in pieces: 
            self.piece_bag.append(piece)

    def _draw_columns_above_grid(self):
        for x in range(COLUMNS):
            for y in range(3):
                shiftedX = (x * BLOCK_SIZE) + TOP_LEFT_X_COORDINATE
                shiftedY = ((y - 3) * BLOCK_SIZE) + TOP_LEFT_Y_COORDINATE
                boardTile = pygame.Rect(shiftedX, shiftedY, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.display, BLACK, boardTile)

    # Draws the playing grid and the placed pieces
    def _draw_grid(self):
        self._draw_columns_above_grid()

        for x in range(COLUMNS):
            for y in range(VISIBLE_ROWS):
                shiftedX = (x * BLOCK_SIZE) + TOP_LEFT_X_COORDINATE
                shiftedY = (y * BLOCK_SIZE) + TOP_LEFT_Y_COORDINATE
                boardSquare = pygame.Rect(shiftedX, shiftedY, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.display, SHAPE_COLORS[self.gameBoard[HIDDEN_ROWS + y, x]], boardSquare)

        pygame.display.flip()

    # Draws the box with the 5 upcoming pieces
    def _draw_upcoming_pieces(self):
        upcomingPiecesDisplayArea = pygame.Rect(
            UPCOMING_PIECES_SCREEN_LEFT_X_COORDINATE, 
            UPCOMING_PIECES_SCREEN_TOP_Y_COORDINATE, 
            UPCOMING_PIECES_SCREEN_WIDTH,
            UPCOMING_PIECES_SCREEN_HEIGHT)
        
        pygame.draw.rect(self.display, WHITE, upcomingPiecesDisplayArea)

        pygame.display.flip()

    # Draws the box with the hold piece
    def _draw_hold_piece(self):
        holdPieceDisplayArea = pygame.Rect(
            HOLD_PIECE_SCREEN_LEFT_X_COORDINATE,
            HOLD_PIECE_SCREEN_TOP_Y_COORDINATE,
            HOLD_PIECE_SCREEN_WIDTH,
            HOLD_PIECE_SCREEN_HEIGHT
        )

        pygame.draw.rect(self.display, WHITE, holdPieceDisplayArea)

        pygame.display.flip()

    # In charge of drawing the falling piece
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

    def _is_falling_piece_legal(self):
        for x in range(self.fallingPiece.width):
            for y in range(self.fallingPiece.height):
                if self.fallingPiece.rotatedPiece[y][x] == '0':
                    xCoord = self.fallingPiece.col + x
                    yCoord = self.fallingPiece.row + y + 20
                    if (xCoord < 0 
                        or xCoord >= COLUMNS
                        or yCoord >= 40
                        or self.gameBoard[yCoord, xCoord] != (len(SHAPE_COLORS) - 1)):
                        return False

        return True

    def _move_falling_piece(self, dx, dy):
        self.fallingPiece.col += dx
        self.fallingPiece.row += dy

        if not self._is_falling_piece_legal():
            self.fallingPiece.col -= dx
            self.fallingPiece.row -= dy
            return False
        return True
    
    def _get_wallkick_table_row(self, rotation) -> List[tuple]:
        rotationIndex = self.fallingPiece.rotation
        match rotation:
            case Rotations.CLOCKWISE:
                # This could be modularized but seems a bit unnecessary rn
                if self.fallingPiece.shapeIdx == 0:
                    return I_PIECE_CLOCKWISE_KICK_TABLE[rotationIndex]
                else:
                    return OTHER_PIECES_CLOCKWISE_KICK_TABLE[rotationIndex]
            case Rotations.COUNTER_CLOCKWISE:
                if self.fallingPiece.shapeIdx == 0:
                    return I_PIECE_COUNTER_CLOCKWISE_KICK_TABLE[rotationIndex]
                else:
                    return OTHER_PIECES_COUNTER_CLOCKWISE_KICK_TABLE[rotationIndex]
            case Rotations.ONE_EIGHTY:
                # There might be a separate one for I pieces idk
                return TETRIO_180_KICK_TABLE[rotationIndex]
            case _:
                return [] # There's a problem
                
    def _handle_wall_kicks(self, rotation):
        tableRow = self._get_wallkick_table_row(rotation)
        initialCol = self.fallingPiece.col
        initialRow = self.fallingPiece.row
        for i in range(len(tableRow)):
            dx, dy = tableRow[i]
            self.fallingPiece.col = initialCol + dx
            self.fallingPiece.row = initialRow + dy
            if self._is_falling_piece_legal():
                return True
        self.fallingPiece.col = initialCol
        self.fallingPiece.row = initialRow

        return False
    
    def _rotate_clockwise(self):
        self.fallingPiece.rotate_clockwise()
        if not self._is_falling_piece_legal():
            # There's a separate kick table for the I piece
            if self._handle_wall_kicks(Rotations.CLOCKWISE):
                return
            self.fallingPiece.reset_setting()
    
    def _rotate_counter_clockwise(self):
        self.fallingPiece.rotate_counter_clockwise()
        if not self._is_falling_piece_legal():
            if self._handle_wall_kicks(Rotations.COUNTER_CLOCKWISE):
                return
            self.fallingPiece.reset_setting()

    def _rotate_180(self):
        self._rotate(Rotations.ONE_EIGHTY)
        if not self._is_falling_piece_legal():
            if self._handle_wall_kicks(Rotations.ONE_EIGHTY):
                return
            self.fallingPiece.reset_setting()

    def _rotate(self, rotation):
        self.fallingPiece.save_original_setting()
        match rotation:
            case Rotations.CLOCKWISE:
                self.fallingPiece.rotate_clockwise()
            case Rotations.COUNTER_CLOCKWISE:
                self.fallingPiece.rotate_counter_clockwise()
            case Rotations.ONE_EIGHTY:
                self.fallingPiece.rotate_180()
            case _:
                raise ValueError("This rotation doesn't exist")

    def _place_falling_piece(self):
        for col in range(self.fallingPiece.width):
            for row in range(self.fallingPiece.height):
                P = self.fallingPiece
                gridRow = P.row + row + HIDDEN_ROWS
                gridCol = P.col + col
                if (P.rotatedPiece[row][col] == '0'):
                    # Please change this later. This is not readable. But basically our color is associated with the shapeIdx
                    self.gameBoard[gridRow, gridCol] = P.shapeIdx 
        self._remove_full_rows()
        self._add_new_falling_piece()

    def _move_piece_to_bottom(self):
        for _ in range(VISIBLE_ROWS - PIECE_SPAWN_HEIGHT_OFFSET):
            self._move_falling_piece(0, 1)

    def _hard_drop(self):
        self._move_piece_to_bottom()
        self._place_falling_piece()
    
    def _soft_drop(self):
        self._move_piece_to_bottom()
    
    # Written by chatgpt
    def _remove_full_rows(self):
        # Find rows that contain the number 7
        mask = np.any(self.gameBoard == 7, axis=1)
        
        # Keep only those rows
        filtered_matrix = self.gameBoard[mask]
        
        # Calculate the number of rows to be filled with 7s
        num_rows_to_fill = self.gameBoard.shape[0] - filtered_matrix.shape[0]
        
        # Create rows filled with 7s
        rows_of_7s = np.full((num_rows_to_fill, self.gameBoard.shape[1]), 7)
        
        # Concatenate the rows of 7s and the filtered matrix
        self.gameBoard = np.vstack((rows_of_7s, filtered_matrix))

                
    # Makes a step in the game
    def play_step(self):
        # List of keys that are pressed
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        print("going left")
                        self._move_falling_piece(-1, 0)
                        self.key_down_time = time.time()
                        self.shifted = False
                    case pygame.K_RIGHT:
                        print("going right")
                        self._move_falling_piece(1, 0)
                        self.key_down_time = time.time()
                        self.shifted = False
                    case pygame.K_DOWN:
                        self._move_piece_to_bottom()
                    case pygame.K_CAPSLOCK:
                        self._add_new_falling_piece()
                        print("Hold this piece")
                    case pygame.K_q:
                        self._rotate_counter_clockwise()
                        print("Rotating CC-wise")
                    case pygame.K_w:
                        self._rotate_clockwise()
                        print("Rotating C-wise")
                    case pygame.K_e:
                        self._rotate_180()
                        print("Rotatin 180")
                    case pygame.K_SPACE:
                        self._hard_drop()
                        print("placed piece")
                    case _:
                        continue

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.key_down_time = None
            self._draw_grid()
            self._draw_falling_piece()

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
