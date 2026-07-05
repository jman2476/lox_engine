from src.game import Game
from src.engines.engine import Engine
from src.functions.find_moves import find_move_notation

class IdiotEngine(Engine):
    def __init__(self, game:Game, side:str):
        super.__init__(self, game, side, 'idiot', 1)
        self.get_pieces = self.game.white if side == 'white' else self.game.black

    def find_moves(self):
        moves = []
        for piece in self.get_pieces():
            moves.append(find_move_notation(self.game, piece))