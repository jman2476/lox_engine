from src.board import Board

class Game():
    def __init__(self,  w_player='Human', b_player='Human'):
        self.board = Board()
        self.w_player = w_player
        self.b_player = b_player
        self.board.setup_new()
        self.fen = ''
        self.pgn = ''
        self.turn = 'white'
        self.halfmove = 0
        self.fullmove = 1
        self.en_passent = ''
        self.castling = ''

    def __repr__(self):
        return self.fen

    def set_fen(self):
        game_board = self.board.board
        fen = ''
        
        for i in range(7, -1, -1):
            count = 0
            for key in game_board:
                piece = game_board[key][i]
                if piece is None:
                    print(piece, f'at {key}{i}')
                else:
                    print(piece)
                if piece is None:
                    count += 1
                    print(count)
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
                print(count, fen)
                fen += f'{count}'
            fen += '/'
        
        fen = fen[:-1] + ' ' + self.turn[0:1]
        fen += ' ' + self.__read_castling() + f'{self.en_passent} {self.halfmove} {self.fullmove}'
        self.fen = fen


    def __read_castling(self):
        game_board = self.board.board
        castle_str = ''
        # check white king, rooks:
        # check a1, e1, h1
        a_one = game_board['a'][0]
        e_one = game_board['e'][0]
        h_one = game_board['h'][0]

        if e_one.name == 'king' and e_one.in_start_pos:
            if h_one.name == 'rook' and h_one.in_start_pos:
                castle_str += 'K'
            if a_one.name == 'rook' and a_one.in_start_pos:
                castle_str += 'Q'

        # check black king, rooks:
        # check a8, e8, h8
        a_eight = game_board['a'][7]
        e_eight = game_board['e'][7]
        h_eight = game_board['h'][7]

        if e_eight.name == 'king' and e_eight.in_start_pos:
            if h_eight.name == 'rook' and h_eight.in_start_pos:
                castle_str += 'k'
            if a_eight.name == 'rook' and a_eight.in_start_pos:
                castle_str += 'q'

        if len(castle_str) == 0:
            castle_str = '-'
        
        self.castling = castle_str
        return castle_str