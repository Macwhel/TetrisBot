from Utils.Movement.DAS import DAS, Direction
from Utils.Movement.Drops import hard_drop, move_piece_to_bottom
from Utils.FallingPiece.AddNewFallingPiece import add_new_falling_piece
import pygame
import numpy as np
import time
from Models.Shapes import SHAPE_COLORS
from Models.Colors import BLACK
from Renders.Grid import draw_falling_piece, draw_grid
from Renders.HoldPiece import draw_hold_piece, draw_hold_piece_background
from Renders.UpcomingPieces import draw_upcoming_pieces
from Utils.FallingPiece.MoveFallingPiece import move_piece
from Utils.Gravity.IncreaseGravity import increase_gravity
from Utils.PieceBag.AddPiecesToBag import add_pieces_to_bag
from Utils.Rotations.Rotations import *
from config import *
from collections import deque

pygame.init()
GRAVITY_EVENT = pygame.USEREVENT + 1
INCREASE_GRAVITY_EVENT = pygame.USEREVENT + 2
"""
TODO: 
transition to throwing all the drawing in another file
add DAS-ing (naive implementation)
Make a class that has fallingPiece and gameBoard
"""


class TetrisGame:
    def __init__(self):
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.key_down_time = None
        self.shifted = False
        pygame.time.set_timer(INCREASE_GRAVITY_EVENT, MILISECONDS_TO_INCREMENT_GRAVITY)
        self.reset()

    def reset(self):
        # initialize game state
        self.display.fill(BLACK)
        self.gameBoard = np.full((40, 10), len(SHAPE_COLORS) - 1)

        # Reset piece bag
        self.pieceBag = deque()
        add_pieces_to_bag(self.pieceBag)
        self.fallingPiece = add_new_falling_piece(self.display, self.pieceBag)
        draw_grid(self.display, self.gameBoard)
        draw_upcoming_pieces(self.display)
        draw_hold_piece_background(self.display)

        # Reset Gravity speed
        self.G = increase_gravity(0, 1 / 60)

        # Hold piece
        self.hold_piece_changed = False
        self.hold_piece = None

    def _hold_piece(self):
        self.fallingPiece.reset_to_original()
        if not self.hold_piece:
            self.hold_piece = self.fallingPiece
            self.fallingPiece = add_new_falling_piece(self.display, self.pieceBag)
        else:
            self.hold_piece, self.fallingPiece = self.fallingPiece, self.hold_piece

        draw_hold_piece(self.display, self.hold_piece)

    # Makes a step in the game
    def play_step(self):
        # List of keys that are pressed
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == INCREASE_GRAVITY_EVENT:
                self.G = increase_gravity(self.G, GRAVITY_INCREMENTATION)
            if event.type == GRAVITY_EVENT:
                move_piece(self.fallingPiece, self.gameBoard, 0, 1)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        print("going left")
                        move_piece(self.fallingPiece, self.gameBoard, -1, 0)
                        self.key_down_time = time.time()
                        self.shifted = False
                    case pygame.K_RIGHT:
                        print("going right")
                        move_piece(self.fallingPiece, self.gameBoard, 1, 0)
                        self.key_down_time = time.time()
                        self.shifted = False
                    case pygame.K_DOWN:
                        move_piece_to_bottom(self.fallingPiece, self.gameBoard)
                    case pygame.K_CAPSLOCK:
                        self._hold_piece()
                        print("Hold this piece")
                    case pygame.K_q:
                        rotate_counter_clockwise(self.fallingPiece, self.gameBoard)
                        print("Rotating CC-wise")
                    case pygame.K_w:
                        rotate_clockwise(
                            self.fallingPiece,
                            self.gameBoard,
                        )
                        print("Rotating C-wise")
                    case pygame.K_e:
                        rotate_180(
                            self.fallingPiece,
                            self.gameBoard,
                        )
                        print("Rotatin 180")
                    case pygame.K_SPACE:
                        self.fallingPiece = hard_drop(
                            self.fallingPiece,
                            self.gameBoard,
                            self.display,
                            self.pieceBag,
                        )
                        print("placed piece")
                    case _:
                        continue

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.key_down_time = None
            draw_grid(self.display, self.gameBoard)
            draw_falling_piece(self.display, self.fallingPiece)

        # Handle DAS
        if self.key_down_time is not None and not self.shifted:
            if time.time() - self.key_down_time > DAS_DELAY:
                if keys[pygame.K_LEFT]:
                    DAS(
                        self.fallingPiece,
                        self.gameBoard,
                        Direction.LEFT,
                    )
                    print("DAS-ing left")
                elif keys[pygame.K_RIGHT]:
                    DAS(
                        self.fallingPiece,
                        self.gameBoard,
                        Direction.RIGHT,
                    )
                    print("DAS-ing right")
                self.shifted = True
                self.key_down_time = None
                draw_grid(self.display, self.gameBoard)
                draw_falling_piece(self.display, self.fallingPiece)


if __name__ == "__main__":
    game = TetrisGame()

    # game loop
    while True:
        game.play_step()

        # if game_over == True:
        # break

    pygame.quit()
