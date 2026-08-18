from src.engines.fast_engine import FastEngine
from src.eval_store import EvalManager, EvalStore
from src.functions.depth_search import DepthChart, crawl_depth_chart
from multiprocessing import Process
import copy, time, random
from queue import Queue
from typing import Self


class SearchArgs():
    def __init__(self, engine:FastEngine, layer:int, parent:DepthChart, move:DepthChart, move_list:list[DepthChart] = []):
        self.engine = engine
        self.layer = layer
        self.parent = parent
        self.move = move
        self.move_list = move_list
        self.idx_path = []

    def add_idx(self, idx:int):
        self.idx_path.append(idx)


class MoveNode():
    def __init__(self, id:str, chart:DepthChart):
        self.id = id
        self.chart = chart
        self.next = []

class MoveArgs():
    def __init__(self, engine:FastEngine, layer: int, parent:str, move:MoveNode):
        self.engine = engine
        self.layer = layer
        self.parent_id = parent
        self.move = move

    def set_next(self, moves:list[MoveNode], engine:FastEngine) -> list[Self]:
        return [
            MoveArgs(engine, self.layer+1, self.move.id, mv)
            for mv in moves
        ]

        
def set_movenode(ch:DepthChart) -> MoveNode:
    node_id = f'{ch.move}{random.seed(f'{ch.eval}{ch.level}{time.time()}')}'
    return MoveNode(node_id, ch)

def depth_search(engine:FastEngine) -> list[DepthChart]:
    # User mp.manager.queue to dynamically add elements to the queue until the desired depth is reached 
    moves = engine.find_ranked_moves()
    mv_charts = [DepthChart(
        mv[0],mv[1], 0, engine.game.turn, engine.game.fen) 
        for mv in moves]
    mv_ch_search_args = [SearchArgs(
        engine, ch.level, None, ch, [])
        for ch in mv_charts]
    max_processes = 4
    results = []

    EvalManager.register('SearchArgs', SearchArgs)
    EvalManager.register('EvalStore', EvalStore)
    with EvalManager() as manager:
        eval_store = manager.EvalStore()
        move_queue = manager.Queue()
        res_list = manager.list()

        eval_store.set_positions(
            engine.eval_store.get_positions())
        for move in mv_ch_search_args:
            move_queue.put(move)

        processes = []
        for i in range(max_processes):
            p = Process(
                target=search_process,
                args=(move_queue, eval_store, res_list),
                name=f"Worker-{i+1}"
            )
            processes.append(p)
            p.start()

        while not move_queue.empty():
            time.sleep(0.01)

        for _ in range(max_processes):
            move_queue.put(None)

        for p in processes:
            p.join()

        engine.eval_store.update_evals(
            eval_store.get_positions()
        )

        print('FDS results:')
        for dch in res_list:
            print(dch)
            for ch in dch.next:
                print(ch)


def search_process(move_queue:Queue, store:EvalStore, results:list[DepthChart]) -> list[SearchArgs]:
    while True:
        move_params = move_queue.get()
        if move_params is None:
            break
        layer = move_params.move.level
        # print(f'Move parameters: {move_params.move}, {move_params.parent}, {move_params.layer}')
        engine_copy = copy.deepcopy(move_params.engine)
        # print(engine_copy.game.board)
        engine_copy.eval_store.update_evals(store.get_positions())

        engine_copy.game.parse_move(move_params.move.move)
        next_moves = engine_copy.find_ranked_moves()
        store.update_evals(engine_copy.eval_store.get_positions())
        
        move_params.move.set_next(next_moves[:engine_copy.breadth],layer, engine_copy.game.turn, engine_copy.game.fen)

        if move_params.layer == 0:
            results.append(move_params.move)
        else:
            for r in results:
                if r == move_params.parent:
                    r.next = move_params.move.next

        if layer < engine_copy.depth:
            next_searches = [
                SearchArgs(
                    engine_copy, ch.level,
                    move_params.move,
                    ch, []
                ) for ch in move_params.move.next
            ]

            for s in next_searches:
                move_queue.put(s)

        move_queue.task_done()

def get_best_move(engine:FastEngine):
    ...


def search_proc_2(move_queueu:Queue, store:EvalStore, node_registry:dict[str, MoveNode]):
    # Must rewrite using TreeNodeArgs!!!!!!
    while True:
        task = move_queueu.get()
        if task is None:
            break

        engine_copy = copy.deepcopy(task.engine)
        layer = task.layer

        engine_copy.eval_store.update_evals(
            store.get_positions()
        )
        engine_copy.game.parse_move(task.move.chart.move)
        next_moves = engine_copy.find_ranked_moves()
        store.update_evals(
            engine_copy.eval_store.get_positions()
        )
        task.move.chart.set_next(
            next_moves[:engine_copy.breadth], layer, engine_copy.game.turn, engine_copy.game.fen
        )
        next_nodes = [
            set_movenode(mv) for mv in task.move.next
        ]

        for n in next_nodes:
            node_registry[n.id] = n

        if layer < engine_copy.depth:
            next_searches = task.set_next(next_nodes, engine_copy)

            for s in next_searches:
                move_queueu.put(s)
            
        move_queueu.task_done()

def depth_search_tree(engine:FastEngine) -> list[DepthChart]:
    # Differs from depth_search by using a dictionary to store
    # all nodes of the search as EvalNodes, to be rebuild into a
    # list[DepthChart] at the end.
    moves = engine.find_ranked_moves()
    turn, fen = engine.game.turn, engine.game.fen
    mv_charts = [
        DepthChart(mv[0], mv[1], 0, turn, fen)
        for mv in moves
    ]
    mv_nodes = [
        set_movenode(mv) for mv in mv_charts
    ]
    mv_args = [
        MoveArgs(engine, 0, None, mv) 
        for mv in mv_nodes
    ]
    ##### Must incorporate tree node args!
    num_processes = 4
    results = []

    EvalManager.register('EvalStore', EvalStore)
    with EvalManager() as manager:
        eval_store = manager.EvalStore()
        move_queue = manager.Queue()
        move_nodes = manager.dict()

        eval_store.set_positions(
            engine.eval_store.get_positions()
        )
        for mv in mv_args:
            move_queue.put(mv)

        processes = []
        for i in range(num_processes):
            p = Process(
                target=search_proc_2,
                args=(move_queue, eval_store, move_nodes),
                name=f'Worker-{i+1}'
            )
            processes.append(p)
            p.start()

        while not move_queue.empty():
            time.sleep(0.01)

        for _ in range(num_processes):
            move_queue.put(None)

        for p in processes:
            p.join()

        engine.eval_store.update_evals(
            eval_store.get_positions()
        )

        return build_tree(move_nodes)

def build_tree(nodes:dict[str, MoveNode]) -> list[DepthChart]:
    list = []