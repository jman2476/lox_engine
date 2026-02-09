from src.functions.parse import parse_square

class Piece():
    def __init__(self, side, square):
        self.side = side.lower()
        self.square = square
        self.file, self.rank = parse_square(self.square)


    def move(self, board, destination):
        # must overide
        pass

    def is_captured(self, board):
        #must override
        pass
    
    def move_valid(self, rank, file):
        pass

    def check_nil_move(self, rank, file):
        if self.rank == rank and self.file == file:
            raise ValueError('Nil move')


class Pawn(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.in_start_pos = True
        self.icon = '\u2659' if self.side == 'white' else '\u265F'

    def move(self, board, destination):
        (file, rank) = parse_square(destination)
        try:
            self.check_nil_move(rank, file)
            self.move_valid(rank, file, board)
            board.board[file][rank-1] = self
            board.board[self.file][self.rank-1] = None
            self.rank, self.file = rank, file 
            self.in_start_pos = False
        except Exception as e:
            print('Pawn move error:', e)
            raise Exception('Pawn move error')

    def move_valid(self, rank, file, board):
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
            raise ValueError(f'Cannot capture own piece at {file}{rank}.')
        
        if self.file == file:
            if dst_occupied:
                raise ValueError('Pawns cannot capture forward')
            if abs(distance) == 2:
                if self.in_start_pos:
                    dst_occupied, dst_side = board.check_square_filled(file, rank-1)
                    if dst_occupied:
                        raise Exception('Moving two squares blocked by another piece')
                    return True
                raise ValueError('Pawns cannot move two square after leaving starting rank')
            elif abs(distance) == 1:
                return True
            else:
                raise ValueError(f'Pawn cannot move distance of {distance} squares')
        else:
            if distance != 1:
                raise ValueError('Too far for pawn to capture')
            elif not dst_occupied:
                raise ValueError('No piece for pawn to capture')
            else:
                return True

class King(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.in_start_pos = True
        self.in_check = False
        self.icon = '\u2654' if self.side == 'white' else '\u265A'

    def move(self, board, destination):
        (file, rank) = parse_square(destination)
        try:
            self.check_nil_move(rank, file)
            self.move_valid(rank, file, board)
            board.board[file][rank-1] = self
            board.board[self.file][self.rank-1] = None
            self.rank, self.file = rank, file 
            self.in_start_pos = False
        except Exception as e:
            print('King move error:', e)
            raise Exception('King move error')
        
    def move_valid(self, rank, file, board):
        # validations for castling/being in check/moving into check will be added later
        if abs(ord(self.file) - ord(file)) > 1 or abs(self.rank - rank) > 1:
            raise ValueError('King cannot move more than 1 square unless castling')
        
        dst_occupied, dst_side = board.check_square_filled(file, rank)
        if not dst_occupied and dst_side == self.side:
            raise ValueError(f'Cannot capture own piece at {file}{rank}.')
        
        return True

class Queen(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2655' if self.side == 'white' else '\u265B'

class Rook(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2656' if self.side == 'white' else '\u265C'
        self.in_start_pos = True

    def move(self, board, destination):
        (file, rank) = parse_square(destination)
        try:
            self.check_nil_move(rank, file)
            self.move_valid(rank, file, board)
            board.board[file][rank-1] = self
            board.board[self.file][self.rank-1] = None
            self.rank, self.file = rank, file 
            self.in_start_pos = False
        except Exception as e:
            print('Rook move error:', e)
            raise Exception('Rook move error')
        
    def move_valid(self, rank, file, board):
        # validations for castling will be added later
        if self.rank != rank and self.file != file:
            print('f', self.file, file)
            print('r', self.rank, rank)
            raise ValueError('Rooks only move vertically and horizontally')
        
        dst_occupied, dst_side = board.check_square_filled(file, rank)
        if not dst_occupied and dst_side == self.side:
            raise ValueError(f'Cannot capture own piece at {file}{rank}.')
        
        if self.rank == rank:
            # positive direction -> right/to h
            # negative direction -> left/ to a
            direction = int((ord(file)-ord(self.file))/abs(ord(self.file)-ord(file)))
            for f_ord in range(ord(self.file), ord(file), direction):
                if f_ord == ord(self.file): continue
                f_char = chr(f_ord)
                blocked, _ = board.check_square_filled(f_char, rank)
                if blocked:
                    raise ValueError(f'There\'s a piece in the way at {f_char}{rank}')
            return True
        if self.file == file:
            # positive direction -> up/  to 8
            # negative direction -> down/to 1
            direction = int((rank - self.rank)/abs(self.rank - rank))
            for r in range(self.rank, rank, direction):
                if r == self.rank: continue
                blocked, _ = board.check_square_filled(self.file, r)
                if blocked:
                    raise ValueError(f'There\'s a piece in the way at {file}{r}')
            return True

class Bishop(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2657' if self.side == 'white' else '\u265D'

    def move(self, board, destination):
        (file, rank) = parse_square(destination)
        try:
            self.check_nil_move(rank, file)
            self.move_valid(rank, file, board)
            board.board[file][rank-1] = self
            board.board[self.file][self.rank-1] = None
            self.rank, self.file = rank, file 
        except Exception as e:
            print('Bishop move error:', e)
            raise Exception('Bishop move error')
        
    def move_valid(self, rank, file, board):
        dist_hor = ord(file) - ord(self.file)
        dist_ver = rank - self.rank

        if abs(dist_hor) != abs(dist_ver):
            raise ValueError('Bishop must move diagonally')
        
        dst_occupied, dst_side = board.check_square_filled(file, rank)
        if not dst_occupied and dst_side == self.side:
            raise ValueError(f'Cannot capture own piece at {file}{rank}.')

        # + -> to h; - -> to a
        dir_hor = int(dist_hor/abs(dist_hor))
        # + -> to 8; - -> to 1
        dir_ver = int(dist_ver/abs(dist_ver))

        rank_check = self.rank + dir_ver
        file_check = chr(ord(self.file) + dir_hor)
        while rank_check != rank or file_check != file:
            print(f'Checking square {file_check}{rank_check}')
            if board.check_square_filled(file_check, rank_check)[0]:
                raise ValueError(f'There\s a piece in the way at {file_check}{rank_check}')
            rank_check += dir_ver
            file_check = chr(ord(file_check) + dir_hor)

        return True

class Knight(Piece):
    def __init__(self, side, square):
        super().__init__(side, square)
        self.icon = '\u2658' if self.side == 'white' else '\u265E'
