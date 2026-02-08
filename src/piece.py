# from .board import Board

class Piece():
    def __init__(self, side, square):
        self.side = side
        self.square = square
        self.parse_square(square)

    def move(self, board, destination):
        # must overide
        pass

    def is_captured(self, board):
        pass

    def parse_square(self, square_string):
        (file, rank) = (square_string[0], square_string[1])
        if ord(rank) not in range(49, 57):
            raise ValueError('parse_square: rank not between 1 and 8')
        if ord(file) not in range(97, 105) and ord(file) not in range(65, 72):
            raise ValueError('parse_square: file not between a and h, or A and H')
        # print(f'Good square: {file}{ord(rank) - 48}')
        return file, ord(rank) - 48
        

class Pawn(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.in_start_pos = True
        self.icon = '\u2659' if self.side == 'white' else '\u265F'


class King(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.can_castle = True
        self.in_check = False
        self.icon = '\u2654' if self.side == 'white' else '\u265A'


class Queen(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2655' if self.side == 'white' else '\u265B'

class Rook(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2656' if self.side == 'white' else '\u265C'

class Bishop(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2657' if self.side == 'white' else '\u265D'

class Knight(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2658' if self.side == 'white' else '\u265E'
