from src.board import Board
from src.functions.parse import parse_square, parse_pawn_move, parse_castling
import copy

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
        print(f'Size of string: {len(string)}')
        last_char = notation_array.pop()
        pieces = self.board.white() if self.turn == 'white' else self.board.black()
        king = next((piece for piece in pieces if piece.name == 'king'))
        checks = self.board.find_checks(king.square, king.side)
        move_board = None
        pawn_move = False

        print(f"Last character of {string}: {last_char}")
        print(f'Is {last_char} in range(1,9)? {last_char in range(1,9)}')


        if last_char == '+' or last_char == '#':
            print('We will handle the checks, thank you')
            last_char = notation_array.pop()
        if last_char in ['Q','N','R','B']:
            print('Looks like pawn promotion!')
            pawn_move = True
            # handle pawn promotion
            # check that there is a pawn in the previous square
            pass
        elif ord(last_char) - 48 in range(1,9):
            print('Standard move type')
            # Standard move type

            # simple pawn move
            if len(string) == 2:
                print('Looks like a pawn move')
                
                move_board = parse_pawn_move(self, string)
                pawn_move = True
            
        elif last_char in ['0', 'o', 'O']:
            print('Looks like castling')
            move_board = parse_castling(self, pieces, king, checks, string)
            
        else:
            print('Some other move')
            pass
        
        # Post move checks:
        new_pieces = move_board.white() if self.turn == 'white' else move_board.black()
        new_king = next((piece for piece in new_pieces if piece.name == 'king'))
        new_checks = self.board.find_checks(new_king.square, new_king.side)

        if new_checks != []:
            print(f'This move would cause checks at {new_checks}')
        else:
            self.board = move_board
            if self.turn == 'black':
                self.fullmove += 1
            self.turn = 'black' if self.turn == 'white' else 'white'
            if not pawn_move:
                self.halfmove += 1
            else:
                self.halfmove = 0

        pass

    