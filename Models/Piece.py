from Models.Shapes import SHAPE_COLORS, SHAPES, shape_height

# TODO: Have each piece have it's own enum value
class Piece(object):
    def __init__(self, col: int, row: int, shapeIdx: int):
        self.col = self.resetCol = self.originalCol = col
        self.row = self.restRow = self.originalRow = row

        self.shapeIdx = shapeIdx
        self.shape = SHAPES[shapeIdx]
        self.color = SHAPE_COLORS[shapeIdx]
        self.rotation = self.resetRotation = 0 # This will be in [0, 3], for four different rotated shapes
        self.update_rotated_piece()

        self.width = len(self.rotatedPiece[0])
        self.height = len(self.rotatedPiece)

        self.piece_width = self.width
        self.piece_height = shape_height(shapeIdx)

    def update_rotated_piece(self):
        self.rotatedPiece = self.shape[self.rotation]

    def rotate_clockwise(self):
        self.rotation = (self.rotation + 1) % 4
        self.update_rotated_piece()

    def rotate_counter_clockwise(self):
        self.rotation = (self.rotation + 3) % 4
        self.update_rotated_piece()

    def rotate_180(self):
        self.rotation = (self.rotation + 2) % 4
        self.update_rotated_piece()

    # Returns a tuple of (col, row, rotation)
    def save_original_setting(self):
        self.resetCol = self.col
        self.resetRow = self.row
        self.resetRotation = self.rotation
    
    # Sets the col, row, and rotation
    def reset_setting(self):
        self.col = self.resetCol
        self.row = self.resetRow
        self.rotation = self.resetRotation

    def reset_to_original(self):
        self.col = self.originalCol
        self.row = self.originalRow
        self.rotation = 0
        self.update_rotated_piece()
