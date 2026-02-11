from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square
from src.functions.diagonals import (
    get_diagonal_edges,
    get_diagonal_squares
    )

class Board():
    def __init__(self):
        self.board = {
                "a":[None for i in range(0,8)],
                "b":[None for i in range(0,8)],
                "c":[None for i in range(0,8)],
                "d":[None for i in range(0,8)],
                "e":[None for i in range(0,8)],
                "f":[None for i in range(0,8)],
                "g":[None for i in range(0,8)],
                "h":[None for i in range(0,8)],
                }
        self.ranks = [i for i in range(0,8)]
        self.files = list("abcdefgh")
        self.frame = (self.ranks, self.files)
        self.white = self.get_white_pieces
        self.black = self.get_black_pieces

    _fen_piece = {
        'p': Pawn,
        'P': Pawn,
        'k': King,
        'K': King,
        'q': Queen,
        'Q': Queen,
        'r': Rook,
        'R': Rook,
        'n': Knight,
        'N': Knight,
        'b': Bishop,
        'B': Bishop
    }    

    def __repr__(self, flip = False):
        dark = False
        files = ' '
        board = ''
        rank_array = [i for i in range(7,-1,-1)]
        
        # Print files:
        for f in self.files:
            files += f' {f}'
        board += files + '\n'

        if flip:
            rank_array.reverse()
        # Print ranks:
        for r in rank_array:
            rank = f'{r+1}'
            for key, file in self.board.items():
                piece = file[r]
                if piece is None: 
                    piece = '\u25A0' if dark else '\u2610'
                else: 
                    piece = piece.icon
                dark = not dark if key != 'h' else dark
                rank += f' {piece}'
            rank += f' {r+1}'
            board += rank + '\n'
        
        board += files + '\n'

        return board

    def setup_new(self):
        for key, file in self.board.items():
            file[0] = self.set_back_rank(key)('white', f'{key}1')
            file[1] = Pawn('white', f'{key}2')
            file[6] = Pawn('black', f'{key}7')
            file[7] = self.set_back_rank(key)('black', f'{key}8')
            
    def setup_by_fen(self, fen_string):
        fen_arr = fen_string.split()
        ranks = fen_arr[0].split('/')

        # iterate from rank 8 to 1 to setup board
        for i in range(7, -1, -1):
            file_ptr = 0
            rank_ptr = 7 - i
            # print('Rank, rankptr', type(ranks[rank_ptr]) , ranks, rank_ptr)
            rank_arr = list(ranks[rank_ptr])
            while len(rank_arr) > 0:
                # print('rank array:', rank_arr)
                char = rank_arr.pop(0)
                if ord(char) in range(49, 57):
                    empties = ord(char) - 48
                    for j in range(0, empties):
                        file = self.files[file_ptr+j]
                        self.board[file][i] = None
                    file_ptr += empties
                    continue
                else:
                    side = 'white' if char.isupper() else 'black'
                    file = self.files[file_ptr]
                    square = f'{file}{i+1}'
                    piece = Board._fen_piece[char](side, square)
                    # print(f'Adding {piece} at {file}{i+1}')
                    self.board[file][i] = piece
                    file_ptr += 1
            # print('Construct with FEN\n',self)
        # set castling rights and pawns' double move rights
        castle_rights = fen_arr[2]
        for f in self.files:
            for r in self.ranks:
                piece = self.board[f][r]
                if piece is None:
                    continue
                if piece.name not in ['pawn', 'rook']:
                    #not checking for kings, because we can set the castling rights based on the rooks
                    continue
                elif piece.name == 'pawn':
                    if piece.side == 'white' and piece.rank != 2:
                        piece.in_start_pos = False
                    elif piece.side == 'black' and piece.rank != 7:
                        piece.in_start_pos = False
                elif piece.name == 'rook':
                    if piece.side == 'white':
                        if 'K' in castle_rights and piece.square == 'h1':
                            continue
                        elif 'Q' in castle_rights and piece.square == 'a1':
                            continue
                        else:
                            piece.in_start_pos = False
                    else:
                        if 'k' in castle_rights and piece.square == 'h8':
                            continue
                        elif 'q' in castle_rights and piece.square == 'h1':
                            continue
                        else:
                            piece.in_start_pos = False
                    
        return fen_arr, ranks

    def set_back_rank(self, file):
        if file == 'a' or file == 'h':
            return Rook
        if file == 'b' or file == 'g':
            return Knight
        if file == 'c' or file == 'f':
            return Bishop
        if file == 'd':
            return Queen
        if file == 'e':
            return King
        raise ValueError('set_back_rank: File value given is out of range')
    
    # Takes a pre-parsed square rank and file
    def check_square_filled(self, file, rank):
        piece = self.board[file][rank-1]
        if piece is None:
            return False, None
        else:
            return True, piece.side
    
    def get_white_pieces(self):
        white_pieces = []
        for i in self.files:
            for j in self.ranks:
                piece = self.board[i][j]
                if piece is None:
                    continue
                if piece.side == 'white':
                    white_pieces.append(piece)
        return white_pieces
    
    def get_black_pieces(self):
        black_pieces = []
        for i in self.files:
            for j in self.ranks:
                piece = self.board[i][j]
                if piece is None:
                    continue
                if piece.side == 'black':
                    black_pieces.append(piece)
        return black_pieces

    def parse_move_notation(self, string):
        pass

    def parse_game_notation(self, string):
        pass

        
    # To use for validating moves, in this order:
    # does move put self in check?
    # does castling move self through check?
    # does move put opponent in check?
    # Order of checks:
    #   - from rooks, queens
    #   - from pawns, bishops, queens
    #   - from knights
    def find_checks(self, king_square, side):
        (king_file, king_rank) = parse_square(king_square)
        checks = []
        directions = [
            'horizontal',
            'vertical',
            'back_diagonal',
            'forward_diagonal',
            'knight'
        ]
        # Iterate through all directions
        for dir in directions:
            pieces = self.next_piece(dir)(king_file, king_rank)
            for piece in pieces:
                if piece is not None and piece.side != side:
                    checks.append(piece)


        return checks
    
    # Nested function to return what pieces 
    # have eyes on a specific square
    def next_piece(self, direction):
        def horizontal(file, rank):
            pieces = [None, None] # a-side, h-side
            side_of_square = 0

            for f in self.files:
                if f == file:
                    side_of_square = 1
                    continue
                piece = self.board[f][rank - 1]
                if piece is None:
                    continue
                elif piece.name == 'queen' or piece.name == 'rook':
                    pieces[side_of_square] = piece
                    if side_of_square == 1:
                        break
                else:
                    pieces[side_of_square] = None

            return pieces
        
        def vertical(file, rank):
            pieces = [None, None] # 1-side, 8-side
            side_of_square = 0

            for r in self.ranks:
                if r == rank-1:
                    side_of_square = 1
                    continue
                piece = self.board[file][r]
                if piece is None:
                    continue
                elif piece.name == 'queen' or piece.name == 'rook':
                    pieces[side_of_square] = piece
                    if side_of_square == 1:
                        break
                else:
                    pieces[side_of_square] = None

            return pieces
        
        def back_diagonal(file, rank):
            pieces = [None, None] # top-left-side, bottom-right-side
            side_of_square = 0
            edges = get_diagonal_edges('back')(file, rank)
            check_squares = get_diagonal_squares(*edges)
            
            for square in check_squares:
                if square[0] == file:
                    side_of_square = 1
                    continue
                piece = self.board[square[0]][square[1]-1]
                
                if piece is None:
                    continue
                elif (piece.name == 'queen'
                      or piece.name == 'bishop'):
                    pieces[side_of_square] = piece
                    if side_of_square == 1:
                        break
                elif piece.name == 'pawn':
                    if (piece.side == 'white' 
                        and side_of_square == 1
                        and abs(piece.rank-rank) == 1):
                        pieces[side_of_square] = piece
                    elif (piece.side == 'black' 
                        and side_of_square == 0
                        and abs(piece.rank-rank) == 1):
                        pieces[side_of_square] = piece
                    else: 
                        pieces[side_of_square] = None
                    if side_of_square == 1:
                        break
                else:
                    pieces[side_of_square] = None
            
            return pieces
        
        def forward_diagonal(file, rank):
            pieces = [None, None] # bottom-left-side, top-right-side
            side_of_square = 0
            edges = get_diagonal_edges('forward')(file, rank)
            check_squares = get_diagonal_squares(*edges)
            
            for square in check_squares:
                if square[0] == file:
                    side_of_square = 1
                    continue
                piece = self.board[square[0]][square[1]-1]
                if piece is None:
                    continue
                elif (piece.name == 'queen'
                      or piece.name == 'bishop'):
                    pieces[side_of_square] = piece
                    if side_of_square == 1:
                        break
                elif piece.name == 'pawn':
                    if (piece.side == 'white' 
                        and side_of_square == 0
                        and abs(piece.rank-rank) == 1):
                        pieces[side_of_square] = piece
                    elif (piece.side == 'black' 
                        and side_of_square == 1
                        and abs(piece.rank-rank) == 1):
                        pieces[side_of_square] = piece
                    else: 
                        pieces[side_of_square] = None
                    if side_of_square == 1:
                        break
                else:
                    pieces[side_of_square] = None

            return pieces
        
        def knight(file, rank):
            pieces = [] 
            file_idx = ord(file)
            squares = [
                (chr(file_idx + 1), rank + 2), # "+2+1; +1+2" (+up+over)
                (chr(file_idx + 2), rank + 1),
                (chr(file_idx + 2), rank - 1), # "-1+2; -2+1"
                (chr(file_idx + 1), rank - 2),
                (chr(file_idx - 1), rank - 2), # "-2-1; -1-2"
                (chr(file_idx - 2), rank - 1),
                (chr(file_idx - 2), rank + 1), # "+1-2; +2-1"
                (chr(file_idx - 1), rank + 2),
            ]
            
            board_squares = []
            for square in squares:
                print(f'Knight square: {square}')
                f, r = square
                if f not in self.files:
                    continue
                if r-1 not in self.ranks:
                    continue
                board_squares.append(square)

            for square in board_squares:
                print(f'Knight culled square: {square}')
                f, r = square
                piece = self.board[f][r-1]
                if piece is None:
                    continue
                elif piece.name == 'knight':
                    pieces.append(piece)

            return pieces

        match direction:
            case 'horizontal':
                return horizontal
            case 'vertical':
                return vertical
            case 'back_diagonal':
                return back_diagonal
            case 'forward_diagonal':
                return forward_diagonal
            case 'knight':
                return knight