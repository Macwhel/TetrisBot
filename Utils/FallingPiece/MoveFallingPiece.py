from Utils.FallingPiece.IsFallingPieceLegal import is_falling_piece_legal


def move_falling_piece(fallingPiece, gameBoard, dx, dy):
    fallingPiece.col += dx
    fallingPiece.row += dy

    if not is_falling_piece_legal(fallingPiece, gameBoard):
        fallingPiece.col -= dx
        fallingPiece.row -= dy
        return False
    return True
