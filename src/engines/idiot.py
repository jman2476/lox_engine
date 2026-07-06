from src.game import Game
from src.engines.engine import Engine
from src.functions.find_moves import find_move_notation
import random

class IdiotEngine(Engine):
    def __init__(self, game:Game, side:str):
        super().__init__(game, side, 'idiot', 1)

    def find_moves(self):
        moves = []
        pieces = self.get_black() if self.game.turn == 'black' else self.get_white()
        for piece in pieces:
            moves.extend(find_move_notation(self.game, piece))
        return moves
    
    def choose_moves(self):
        # This engine is meant to play randomly, so it will randomly choose 3 moves
        selection = set()
        moves = self.find_moves()
        max = len(moves)
        while len(selection) < 5 and len(selection) < max:
            selection.add(random.choice(moves))

        return list(selection)
    
    def pick_and_play_move(self):
        print(self.game.board)
        move = random.choice(self.choose_moves())
        self.game.parse_move(move)
        print(self.game.board)
            
