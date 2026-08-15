from src.engines.fast_engine import FastEngine
from src.eval_store import EvalManager, EvalStore
from src.functions.depth_search import DepthChart, crawl_depth_chart
from multiprocessing import Process
import copy, time
from queue import Queue


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
    mv_ch_search_args = [SearchArgs(
        engine, ch.level, None, ch, [])
        for ch in mv_charts]
    results = []

    EvalManager.register('SearchArgs', SearchArgs)
    EvalManager.register('EvalStore', EvalStore)
    with EvalManager() as manager:
        eval_store = manager.EvalStore()
        move_queue = manager.Queue()

        eval_store.set_positions(
            engine.eval_store.get_positions())
        for move in mv_ch_search_args:
            move_queue.put(move)

        processes = []
        for i in range(4):
            p = Process(
                target=search_process,
                args=(move_queue, eval_store),
                name=f"Worker-{i+1}"
            )
            processes.append(p)
            p.start()

        while not move_queue.empty():
            time.sleep(0.01)

        for _ in range(4):
            move_queue.put(None)

        for p in processes:
            p.join()

        engine.eval_store.update_evals(
            eval_store.get_positions()
        )


def search_process(move_queue:Queue, store:EvalStore) -> list[SearchArgs]:
    move_params = move_queue.get()
    engine_copy = copy.deepcopy(move_params.engine)
    engine_copy.game.parse_move()

    move_queue.task_done()

def get_best_move(engine:FastEngine):
    ...