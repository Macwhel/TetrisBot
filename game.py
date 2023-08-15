from Models.Stats import Stats
from Renders.Stats import draw_apm, draw_pps, draw_timer
from Renders.UpcomingPieces import draw_upcoming_pieces
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
from Utils.FallingPiece.MoveFallingPiece import move_piece
from Utils.Gravity.IncreaseGravity import increase_gravity
from Utils.PieceBag.AddPiecesToBag import add_pieces_to_bag
from Utils.Rotations.Rotations import *
from Utils.Time.ParseElapsedTime import parseElapsedTime
from config import *
from collections import deque

pygame.init()
GRAVITY_EVENT = pygame.USEREVENT + 1
INCREASE_GRAVITY_EVENT = pygame.USEREVENT + 2
"""
TODO:
Have hardcoded "images" of the pieces that I can just throw onto the queue or smth
Draw the upcoming pieces
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
        self.font = pygame.font.Font(None, 36)

        self.reset()

    def reset(self):
        # initialize game state
        self.display.fill(BLACK)
        self.gameBoard = np.full((40, 10), len(SHAPE_COLORS) - 1)

        # Reset piece bag
        self.pieceBag = deque()
        add_pieces_to_bag(self.pieceBag)
        self.fallingPiece, self.already_held = add_new_falling_piece(
            self.display, self.pieceBag
        )
        draw_grid(self.display, self.gameBoard)
        draw_upcoming_pieces(self.display, self.pieceBag)
        draw_hold_piece_background(self.display)

        # Reset Gravity speed
        self.G = increase_gravity(0, 1 / 60)

        # Hold piece
        self.hold_piece_changed = False
        self.hold_piece = None

        # Reset last rendered values
        self.last_rendered_timer_value = None
        self.last_rendered_pps_value = None
        self.last_rendered_apm_value = None

        # Reset number of pieces placed
        self.pieces_placed = 0

        # Reset the statistics
        self.stats = Stats()

    # This shit is a bit annoying to refactor
    def _hold_piece(self):
        if not self.already_held:
            self.fallingPiece.reset_to_original()
            if not self.hold_piece:
                self.hold_piece = self.fallingPiece
                self.fallingPiece, _ = add_new_falling_piece(
                    self.display, self.pieceBag
                )
            else:
                self.hold_piece, self.fallingPiece = self.fallingPiece, self.hold_piece

            self.already_held = True
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
                        move_piece(self.fallingPiece, self.gameBoard, -1, 0)
                        self.key_down_time = time.time()
                        self.shifted = False
                    case pygame.K_RIGHT:
                        move_piece(self.fallingPiece, self.gameBoard, 1, 0)
                        self.key_down_time = time.time()
                        self.shifted = False
                    case pygame.K_DOWN:
                        move_piece_to_bottom(self.fallingPiece, self.gameBoard)
                    case pygame.K_CAPSLOCK:
                        self._hold_piece()
                    case pygame.K_q:
                        rotate_counter_clockwise(self.fallingPiece, self.gameBoard)
                    case pygame.K_w:
                        rotate_clockwise(
                            self.fallingPiece,
                            self.gameBoard,
                        )
                    case pygame.K_e:
                        rotate_180(
                            self.fallingPiece,
                            self.gameBoard,
                        )
                    case pygame.K_SPACE:
                        (
                            self.fallingPiece,
                            self.already_held,
                        ), self.gameBoard = hard_drop(
                            self.fallingPiece,
                            self.gameBoard,
                            self.display,
                            self.pieceBag,
                            self.stats.incrementTotalPiecesPlaced,
                        )
                    case pygame.K_r:
                        self.reset()
                    case _:
                        continue

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.key_down_time = None
                    self.shifted = False

            if self.shifted:
                if keys[pygame.K_LEFT]:
                    DAS(
                        self.fallingPiece,
                        self.gameBoard,
                        Direction.LEFT,
                    )
                elif keys[pygame.K_RIGHT]:
                    DAS(
                        self.fallingPiece,
                        self.gameBoard,
                        Direction.RIGHT,
                    )

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
                elif keys[pygame.K_RIGHT]:
                    DAS(
                        self.fallingPiece,
                        self.gameBoard,
                        Direction.RIGHT,
                    )
                self.currentlyDASing = True
                self.shifted = True
                self.key_down_time = None
                draw_grid(self.display, self.gameBoard)
                draw_falling_piece(self.display, self.fallingPiece)

        minutes, seconds, milliseconds = self.stats.getMinutesSecondsMilliseconds()

        if (minutes, seconds, milliseconds) != self.last_rendered_timer_value:
            # If the value changed, update last rendered timer value
            self.last_rendered_timer_value = (minutes, seconds, milliseconds)

            draw_timer(self.font, self.display, minutes, seconds, milliseconds)

        apm = self.stats.getAPM()
        if apm != self.last_rendered_apm_value:
            self.last_rendered_apm_value = apm
            draw_apm(self.font, self.display, self.stats)

        pps = self.stats.getPPS()
        if pps != self.last_rendered_pps_value:
            self.last_rendered_pps_value = pps
            draw_pps(self.font, self.display, self.stats)


if __name__ == "__main__":
    game = TetrisGame()

    # game loop
    while True:
        game.play_step()

        # if game_over == True:
        # break

    pygame.quit()
