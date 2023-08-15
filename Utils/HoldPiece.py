from Renders.HoldPiece import draw_hold_piece
from Utils.FallingPiece.AddNewFallingPiece import add_new_falling_piece


def hold_piece(self):
    self.fallingPiece.reset_to_original()
    if not self.hold_piece:
        self.hold_piece = self.fallingPiece
        self.fallingPiece = add_new_falling_piece(self.display, self.pieceBag)
    else:
        self.hold_piece, self.fallingPiece = self.fallingPiece, self.hold_piece

    draw_hold_piece(self.display, self.hold_piece)
