from src.game import Game
from src.engines.engine import Engine
from src.functions.find_moves import find_move_notation
import random

class FoolEngine(Engine):
    def __init__(self, game:Game, side:str):
        super().__init__(game, side, 'fool', 1)

    def find_moves(self):
        moves = []
        pieces = self.white if self.game.turn == 'white' else self.black
        for piece in pieces:
            moves.extend(find_move_notation(self.game, piece))
        # Debugging: print moves w/ notation
        print(f'Moves: {moves}')
        return moves
    
    def choose_moves(self):
        # This engine is meant to play randomly, so it will randomly choose 3 moves
        selection = set()
        moves = self.find_moves()
        if len(moves) < 5:
            return moves
        max = len(moves)
        while len(selection) < 5 and len(selection) < max:
            selection.add(random.choice(moves))

        return list(selection)
    
    def pick_and_play_move(self):
        print(self.game.board)
        self.white = self.game.board.white()
        self.black = self.game.board.black()
        move = random.choice(self.choose_moves())
        try:
            self.game.parse_move(move)
            print(self.game.board)
        except Exception as e:
            print(f'Engine error: could not play move {move} because {e}')
