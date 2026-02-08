from .functions.parse import parse_square

class Piece():
    def __init__(self, side, square):
        self.side = side
        self.square = square
        self.file, self.rank = parse_square(self.square)


    def move(self, board, destination):
        # must overide
        pass

    def is_captured(self, board):
        #must override
        pass
    
    def move_valid_for_piece(self, rank, file):
        pass

    
        

class Pawn(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.in_start_pos = True
        self.icon = '\u2659' if self.side == 'white' else '\u265F'

    def move(self, board, destination):
        (file, rank) = parse_square(destination)
        try:
            self.move_valid_for_piece(rank, file, board)
            board.board[file][rank] = self
            board.board[self.file][self.rank] = None
            self.rank, self.file = rank, file 
        except Exception as e:
            print('Pawn move error:', e)
            raise Exception('Pawn move error')

    def move_valid_for_piece(self, rank, file, board):
        if self.rank == rank:
            raise ValueError('Pawns cannot move laterally')
        elif (self.rank > rank and self.side == 'white'):
            raise ValueError('Pawns cannot move backwards')
        elif (self.rank < rank and self.side == 'black'):
            raise ValueError('Pawns cannot move backwards')
        if abs(ord(self.file) - ord(file)) > 1:
            raise ValueError('Pawns cannot move more than one file over')
        
        distance = rank - self.rank
        dst_occupied, dst_side = board.check_square_filled(file, rank)
        if not dst_occupied and dst_side == self.side:
            return Exception(f'Cannot capture own piece at {file}{rank}.')
        
        if self.file == file:
            if dst_occupied:
                raise Exception('Pawns cannot capture forward')
            if abs(distance) == 2:
                if self.in_start_pos:
                    return True
                raise Exception('Pawns cannot move two square after leaving starting rank')
            elif abs(distance) == 1:
                return True
            else:
                raise Exception(f'Pawn cannot move distance of {distance} squares')
        else:
            if distance != 1:
                raise Exception('Too far for pawn to capture')
            elif not dst_occupied:
                raise Exception('No piece for pawn to capture')
            else:
                return True

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
