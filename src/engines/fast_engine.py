from src.engines.engine import Engine
from src.functions.evaluation import get_evaluation
from src.functions.find_moves import find_move_notation
from src.game import Game
from typing import Literal
from src.eval_store import EvalStore, EvalManager
import copy, logging
from multiprocessing import Process

class FastEngine(Engine):
    def __init__(self, game:Game, 
                 side:Literal['white', 'black'], 
                 search:tuple[int,int]=(2,2)):
        super().__init__(game, side, 'fast', search[0])
        self.breadth = search[1]
        self.search = search
        self.eval_store = EvalStore()

    def find_moves(self) -> list[str]:
        self.white = self.game.board.white()
        self.black = self.game.board.black()
        pieces = self.white if self.game.turn == 'white' else self.black
        moves = []
        for p in pieces:
            moves.extend(find_move_notation(self.game, p))
        print(f'Available engine moves: {moves}')
        return moves

    def rank_moves(self, eval_moves:list[tuple[str,float]]
                   ) -> list[(str,float)]:
        ...

    def eval_moves(self, move:str
                    ) -> list[tuple[str, float]]:
        ...
