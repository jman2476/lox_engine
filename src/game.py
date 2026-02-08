from .board import Board

class Game():
    def __init__(self,  w_player=None, b_player=None):
        self.board = Board()
        self.w_player = w_player
        self.b_player = b_player
        self.board.setup_new()
        self.fen = ''
        self.pgn = ''
