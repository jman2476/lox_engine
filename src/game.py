from src.board import Board
from src.functions.parse import (
    parse_square, 
    parse_pawn_move, 
    parse_castling, 
    parse_pawn_promotion,
    parse_pawn_capture,
    parse_piece_move
    )
from src.functions.find_moves import (
    find_king_moves,
    find_available_moves
    )
from src.pgn_writer import PGNWriter
import copy

class Game():
    def __init__(self,  w_player='Human', b_player='Human'):
        self.board = Board()
        self.w_player = w_player
        self.b_player = b_player
        self.fen = ''
        self.pgnw = PGNWriter(self)
        self.turn = 'white'
        self.halfmove = 0
        self.fullmove = 1
        self.en_passent = '-'
        self.castling = '-'
        self.winner = None
        self.set_fen()
        self.board_states = {}

    def __repr__(self):
        self.set_fen()
        return self.fen
    
    def start_new_game(self):
        self.board.setup_new()
        self.set_fen()
        self.__add_board_state()
        self.pgnw.create_file()

    def set_fen(self):
        game_board = self.board.board
        fen = ''
        
        for i in range(7, -1, -1):
            count = 0
            for key in game_board:
                piece = game_board[key][i]
                if piece is None:
                    count += 1
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

    def __add_board_state(self):
        board_fen = self.fen.split()[0]
        if board_fen in self.board_states:
            self.board_states[board_fen] += 1
            if self.board_states[board_fen] >=3:
                self.winner = '1/2-1/2'
        else:
            self.board_states[board_fen] = 1

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
            # else:
            #     print('--Black Queen side castling read--')
            #     print(f'a8: {a_eight}')
            #     if a_eight is not None:
            #         print(f'Name: {a_eight.name}, in start position: {a_eight.in_start_pos}')

        if len(castle_str) == 0:
            castle_str = '-'
        
        self.castling = castle_str
        return castle_str
    
    def get_castle_state(self):
        self.__read_castling()
        return self.castling
    
    def parse_move(self, string, is_game_call=True, is_eval_call=False):
        notation_array = list(string)
        last_char = notation_array.pop()
        pieces = self.board.white() if self.turn == 'white' else self.board.black()
        king = next((piece for piece in pieces if piece.name == 'king'))
        checks = self.board.find_checks(king.square(), king.side)
        move_board = self.board
        pawn_move = False
        capture_move = False
        initial_ep = self.en_passent

        try:
            if last_char == '+' or last_char == '#':
                # print('We will handle the checks, thank you')
                last_char = notation_array.pop()
                if '+' in string or '#' in string:
                    string = string[0:-1]
                # print(f'new last_char: {last_char}, new string {string}')
            if last_char in ['Q','N','R','B']:
                # print('Looks like pawn promotion!')
                move_board = parse_pawn_promotion(self, string)
                pawn_move = True
                # handle pawn promotion
                # check that there is a pawn in the previous square
            elif last_char in ['0', 'o', 'O']:
                # print('Looks like castling')
                move_board = parse_castling(self, pieces, king, checks, string)
            elif int(last_char) in range(1,9):
                # print('Standard move type')
                # Standard move type
                
                # simple pawn move
                if len(string) == 2:
                    # print('Looks like a pawn move')
                    move_board = parse_pawn_move(self, string)
                    pawn_move = True
                elif string[0] in move_board.files:
                    # print('Looks like a pawn capture')
                    move_board = parse_pawn_capture(self, string)
                    pawn_move = True
                elif string[0] in move_board._fen_piece:
                    # parse piece move
                    move_board, capture_move = parse_piece_move(self, string)
                
            else:
                print(f'Some unknown move: {string}')
        except Exception as e:
            print(f'Error found: {e}')
            raise e
        finally:   
            # Post move checks:
            new_pieces = move_board.white() if self.turn == 'white' else move_board.black()
            new_king = next((piece for piece in new_pieces if piece.name == 'king'))
            new_checks = move_board.find_checks(new_king.square(), new_king.side)
            move_happened = False
            if move_board == self.board:
                print('No move happened')
                self.en_passent = initial_ep
            elif new_checks != []:
                self.en_passent = initial_ep
            else: # move succeeds
                self.board = move_board
                move_happened = True
                if is_game_call:
                    opp_pieces = self.board.white() if self.turn == 'black' else self.board.black()
                    opp_king = next((p for p in opp_pieces if p.name == 'king'))
                    check = 0 < len(self.board.find_checks(opp_king.square(), opp_king.side))
                    self.pgnw.add_move(string, check)
                if self.turn == 'black':
                    self.fullmove += 1
                self.turn = 'black' if self.turn == 'white' else 'white'
                # show checkmate validator
                if not (pawn_move or capture_move):
                    self.halfmove += 1
                else: 
                    self.halfmove = 0
                if self.en_passent != '-' and self.en_passent == initial_ep:
                    self.en_passent = '-'
            self.set_fen()
            if move_happened:
                self.__add_board_state()
                if is_game_call or is_eval_call:
                    if self.turn == 'white':
                        end = self.is_checkmated('white', is_eval_call)
                        if end:
                            print('Looks like white has been checkmated')
                            self.winner = '0-1'
                            if is_game_call:
                                self.pgnw.final_result()
                    else:
                        end = self.is_checkmated('black', is_eval_call)
                        if end:
                            print('Looks like black has been checkmated')
                            self.winner = '1-0'
                            if is_game_call:
                                self.pgnw.final_result()
    
    # placing this in main game loop causes infinite recursion loop
    def is_checkmated(self, side:str, is_eval:bool=False) -> bool:
        # print('looking for checkmate')
        from src.piece import King
        king = None
        pieces = []
        if side == 'white':
            pieces = self.board.white()
            king = [k for k in pieces if isinstance(k, King)][0]
        else:
            pieces = self.board.black()
            king = [k for k in pieces if isinstance(k, King)][0]


        game_copy = copy.deepcopy(self)
        checks = self.board.find_checks(king.square(), king.side)
        move_lists = [find_available_moves(game_copy, p) for p in pieces]
        moves = []
        for ls in move_lists:
            moves.extend(ls)
        # print(f'moves: {moves}\nchecks: {checks}')
        if len(checks) > 0 and len(moves) == 0:
            if side == 'white':
                self.winner = 'black'
            else:
                self.winner = 'white'
            return True
        self.handle_stalemate(checks, moves, is_eval)
        self.handle_fifty_move_rule(is_eval)
        return False
    
    def handle_stalemate(self, checks, moves, is_eval=False):
        if (len(checks) == 0 and len(moves) == 0
            or not self.board.sufficient_material()):
            self.winner = '1/2-1/2'
            if not is_eval:
                self.pgnw.final_result()

    def handle_fifty_move_rule(self, is_eval=False):
        if self.halfmove >= 50:
            self.winner = '1/2-1/2'
            if not is_eval:
                self.pgnw.final_result()
    
    