from src.piece import Piece, Pawn, King, Queen, Bishop, Knight, Rook
from src.functions.parse import parse_square

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
    
    def parse_move_notation(self, string):
        pass

    def parse_game_notation(self, string):
        pass

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