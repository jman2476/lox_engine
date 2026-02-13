from src.board import Board
from src.functions.parse import parse_square

class Game():
    def __init__(self,  w_player='Human', b_player='Human'):
        self.board = Board()
        self.w_player = w_player
        self.b_player = b_player
        self.fen = ''
        self.pgn = ''
        self.turn = 'white'
        self.halfmove = 0
        self.fullmove = 1
        self.en_passent = '-'
        self.castling = '-'
        self.winner = None
        self.set_fen()

    def __repr__(self):
        return self.fen
    
    def start_new_game(self):
        self.board.setup_new()
        self.set_fen()

    def set_fen(self):
        game_board = self.board.board
        fen = ''
        
        for i in range(7, -1, -1):
            count = 0
            for key in game_board:
                piece = game_board[key][i]
                # if piece is None:
                #     print(piece, f'at {key}{i}')
                # else:
                #     print(piece)
                if piece is None:
                    count += 1
                    # print(count)
                else:
                    char = piece.name[0]
                    if piece.name == 'knight':
                        char = 'n'
                    if piece.side == 'white':
                        char = char.capitalize()
                    if count > 0:

                        fen += f'{count}'
                        count = 0
                    fen += char
            if count > 0:
                # print(count, fen)
                fen += f'{count}'
            fen += '/'
        
        fen = fen[:-1] + ' ' + self.turn[0:1]
        fen += ' ' + self.__read_castling() + f' {self.en_passent} {self.halfmove} {self.fullmove}'
        self.fen = fen

    def read_fen(self, fen_string):
        fen_arr = fen_string.split()
        self.fen = fen_string
        self.turn = 'white' if fen_arr[1] == 'w' else 'black'
        self.castling = fen_arr[2]
        self.en_passent = fen_arr[3]
        self.halfmove = int(fen_arr[4])
        self.fullmove = int(fen_arr[5])
        self.board.setup_by_fen(fen_string)


    def __read_castling(self):
        game_board = self.board.board
        castle_str = ''
        # check white king, rooks:
        # check a1, e1, h1
        a_one = game_board['a'][0]
        e_one = game_board['e'][0]
        h_one = game_board['h'][0]

        if (e_one is not None
            and e_one.name == 'king' 
            and e_one.in_start_pos):
            if (h_one is not None
                and h_one.name == 'rook' 
                and h_one.in_start_pos):
                castle_str += 'K'
            if (a_one is not None
                and a_one.name == 'rook' 
                and a_one.in_start_pos):
                castle_str += 'Q'

        # check black king, rooks:
        # check a8, e8, h8
        a_eight = game_board['a'][7]
        e_eight = game_board['e'][7]
        h_eight = game_board['h'][7]

        if (e_eight is not None
            and e_eight.name == 'king' 
            and e_eight.in_start_pos):
            if (h_eight is not None 
                and h_eight.name == 'rook' 
                and h_eight.in_start_pos):
                castle_str += 'k'
            if ( a_eight is not None
                and a_eight.name == 'rook' 
                and a_eight.in_start_pos):
                castle_str += 'q'

        if len(castle_str) == 0:
            castle_str = '-'
        
        self.castling = castle_str
        return castle_str
    
    def get_castle_state(self):
        self.__read_castling()
        return self.castling
    
    def parse_move(self, string):
        notation_array = list(string)
        last_char = notation_array.pop()
        pieces = self.board.white() if self.turn == 'white' else self.board.black()
        king = next((piece for piece in pieces if piece.name == 'king'))
        checks = self.board.find_checks(king.square, king.side)
        print(f"Last character of {string}: {last_char}")

        if last_char == '+' or last_char == '#':
            last_char = notation_array.pop()
        if last_char in ['Q','N','R','B']:
            # handle pawn promotion
            # check that there is a pawn in the previous square
            pass
        elif last_char in range(1,9):
            # Standard move type

            # simple pawn move
            if len(string) == 2:
                file, rank = string[0], string[1]
                pawn_rank = rank - 1 if self.turn == 'white' else rank -1
                piece = self.board.board[file][pawn_rank-1]
                if piece is None:
                    if rank in [4,5]:
                        piece = self.board.board[file][pawn_rank-1] 
                    raise ValueError('Pawn move error: no pawn found')
                elif piece.name != 'pawn':
                    raise ValueError('Pawn move error: piece in previous square is not a pawn')

            pass
        elif last_char in ['0', 'o', 'O']:
            rooks = [piece for piece in pieces if piece.name == 'rook']
            for rook in rooks:
                print(rook)
            if string in ['0-0', 'O-O', 'o-o']:
                h_rook = next((rook for rook in rooks 
                               if (rook.square == 'h1' or rook.square == 'h8')))
                print(f'a_rook: {h_rook}, {h_rook.in_start_pos}')
                if h_rook is None or not h_rook.in_start_pos:
                    raise ValueError(
                        'Castling failure: The h rook has been moved off starting square')
                elif not king.in_start_pos:
                    raise ValueError(
                        'Castling failure: King has moved off of starting square'
                    )
                elif len(checks) > 0:
                    print(f'Checks: {checks}')
                    raise ValueError(
                        f'Castling failure: King is in check'
                    )
                
                # handle castling
                # will king move through check on f and g files?
                (f_sqr, g_sqr) = ('f' + king.square[1],
                                    'g' + king.square[1])
                print(f'Squares to check during castling: {f_sqr}{g_sqr}')
                f_file, f_rank = parse_square(f_sqr)
                g_file, g_rank = parse_square(g_sqr)
                blocked = (self.board.check_square_filled(f_file,f_rank)[0],
                            self.board.check_square_filled(g_file,g_rank)[0])
                if True in blocked:
                    raise ValueError(
                        'Castling error: Castling movement is blocked by a piece')

                f_check, g_check = (self.board.find_checks(f_sqr, king.side),
                                    self.board.find_checks(g_sqr, king.side))
                if len(f_check) > 0 or len(g_check) > 0:
                    print(f'Threats on f square: {f_check}')
                    print(f'Threats on g square: {g_check}')
                    raise ValueError(
                        'Castling error: King would move through check to castle')

                self.board.board['g'][g_rank-1] = king
                self.board.board['f'][f_rank-1] = h_rook
                self.board.board[king.file][king.rank-1] = None
                self.board.board[h_rook.file][h_rook.rank-1] = None
                king.square = g_sqr
                h_rook.square = f_sqr
                print(f'Post move board: \n{self.board}')
            elif string in ['0-0-0', 'o-o-o', 'O-O-O']:
                a_rook = next((rook for rook in rooks 
                               if (rook.square == 'a1' or rook.square == 'a8')))
                if a_rook is None or not a_rook.in_start_pos:
                    print(f'a_rook: {a_rook}, {a_rook.in_start_pos}')
                    raise ValueError(
                        'Castling failure: The a rook has been moved off starting square')
                elif not king.in_start_pos:
                    raise ValueError(
                        'Castling failure: King has moved off of starting square'
                    )
                elif len(checks) > 0:
                    print(f'Checks: {checks}')
                    raise ValueError(
                        f'Castling failure: King is in check'
                    )
                
                # handle castling
                # will king move through check on f and g files?
                (d_sqr, c_sqr) = ('d' + king.square[1],
                                    'c' + king.square[1])
                print(f'Squares to check during castling: {d_sqr}{c_sqr}')
                d_file, d_rank = parse_square(d_sqr)
                c_file, c_rank = parse_square(c_sqr)
                blocked = (self.board.check_square_filled(d_file,d_rank)[0],
                            self.board.check_square_filled(c_file,c_rank)[0])
                if True in blocked:
                    raise ValueError(
                        'Castling error: Castling movement is blocked by a piece')

                d_check, c_check = (self.board.find_checks(d_sqr, king.side),
                                    self.board.find_checks(c_sqr, king.side))
                if len(d_check) > 0 or len(c_check) > 0:
                    print(f'Threats on d square: {d_check}')
                    print(f'Threats on c square: {c_check}')
                    raise ValueError(
                        'Castling error: King would move through check to castle')

                self.board.board['c'][c_rank-1] = king
                self.board.board['d'][d_rank-1] = a_rook
                self.board.board[king.file][king.rank-1] = None
                self.board.board[a_rook.file][a_rook.rank-1] = None
                king.square = c_sqr
                a_rook.square = d_sqr
                print(f'Post move board: \n{self.board}')
            else:
                raise ValueError(
                    'Invalid move syntax. Suspected castling move.')
            
        else:
            pass
         
        pass