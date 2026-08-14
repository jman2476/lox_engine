from src.engines.fast_engine import FastEngine
from src.eval_store import EvalManager, EvalStore
from src.functions.depth_search import DepthChart, crawl_depth_chart
from multiprocessing import Process
import copy

class SearchArgs():
    def __init__(self, engine:FastEngine, layer:int, parent:DepthChart, move:DepthChart, move_list:list[DepthChart] = []):
        self.engine = engine
        self.layer = layer
        self.parent = parent
        self.move = move
        self.move_list = move_list


def depth_search(engine:FastEngine) -> list[DepthChart]:
    # User mp.manager.queue to dynamically add elements to the queue until the desired depth is reached 
    moves = engine.find_ranked_moves()
    mv_charts = [DepthChart(
        mv[0],mv[1], 0, engine.game.turn, engine.game.fen) 
        for mv in moves]

def search_process(params:SearchArgs) -> list[SearchArgs]:
    engine_copy = copy.deepcopy(params.engine)
    engine_copy.game.parse_move()

def get_best_move(engine:FastEngine):
    ...