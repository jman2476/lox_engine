from src.engines.fast_engine import FastEngine
from src.eval_store import EvalManager, EvalStore
from src.functions.depth_search import DepthChart, crawl_depth_chart
from multiprocessing import Process
import copy

class SearchArgs():
    def __init__(self, engine:FastEngine, layer:int, parent:DepthChart, move_list:list[DepthChart]):
        self.engine = engine
        self.layer = layer
        self.parent = parent
        self.move_list = move_list


def depth_search(engine:FastEngine) -> list[DepthChart]:
    ...

def search_process(params:SearchArgs) -> list[SearchArgs]:
    ...

def get_best_move(engine:FastEngine):
    ...