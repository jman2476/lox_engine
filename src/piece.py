

class Piece():
    def __init__(self, side, square):
        self.side = side
        self.square = square
        

class Pawn(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.in_start_pos = True
        self.icon = '\u2659' if self.side is 'white' else '\u265F'


class King(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.can_castle = True
        self.in_check = False
        self.icon = '\u2654' if self.side is 'white' else '\u265A'


class Queen(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2655' if self.side is 'white' else '\u265B'

class Rook(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2656' if self.side is 'white' else '\u265C'

class Bishop(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2657' if self.side is 'white' else '\u265D'

class Knight(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2658' if self.side is 'white' else '\u265E'
