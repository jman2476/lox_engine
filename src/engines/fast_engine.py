from src.engines.engine import Engine
from src.game import Game
from typing import Literal
from src.eval_store import EvalStore

class FastEngine(Engine):
    def __init__(self, game:Game, 
                 side:Literal['white', 'black'], 
                 search:tuple[int,int]=(2,2)):
        super().__init__(game, side, 'fast', search[0])
        self.breadth = search[1]
        self.search = search
        self.eval_store = EvalStore()