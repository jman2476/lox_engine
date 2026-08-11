from src.engines.engine import Engine
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

    def find_moves(self, game:Game) -> list[str]:
        ...

    def rank_moves(self, eval_moves:list[tuple[str,float]]
                   ) -> list[(str,float)]:
        ...

    def eval_move_process(self, move:str
                          ) -> tuple[str, float]:
        ...

    def eval_moves_mp(self, move_list:list[str]
                      ) -> list[tuple[str,float]]:
        ...