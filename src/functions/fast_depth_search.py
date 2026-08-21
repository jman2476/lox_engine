from src.engines.fast_engine import FastEngine
from src.eval_store import EvalManager, EvalStore
from src.functions.depth_search import DepthChart, crawl_depth_chart
from multiprocessing import Process
import copy, time, random
from queue import Queue
from typing import Self
import logging
logger = logging.getLogger(__name__)


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

    def __repr__(self):
        return f'Move Node: ID {self.id}\nNext: {self.next}\nChart:{self.chart}'

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

class KeyChain():
    def __init__(self, manager:EvalManager):
        self.counter = manager.Lock()
        self.store = manager.Lock()
        self.registry = manager.Lock()

    def get_counter(self):
        return self.counter

    def get_store(self):
        return self.store

    def get_registry(self):
        return self.registry
        
def set_movenode(ch:DepthChart) -> MoveNode:
    random.seed(f'{ch.eval}{ch.level}{time.time()}')
    rand_part = int(random.random()*1e6)
    # print(f'New node rand part: {rand_part}')
    node_id = f'{ch.move}{rand_part}'
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

    EvalManager.register('SearchArgs', SearchArgs)
    EvalManager.register('EvalStore', EvalStore)
    EvalManager.register('KeyChain', KeyChain)
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

        engine_copy.game.parse_move(move_params.move.move, False, True)
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
    move_tree = depth_search_tree(engine)
    logger.info(f'{engine.game.turn}\'s moves:\n{move_tree}')
    crawls = []
    for ch in move_tree:
        crawl = crawl_depth_chart(ch)
        if crawl[3] is None:
            crawl[3] = crawl[1]
            crawl[4] = crawl[2]
        crawls.append(crawl)
    if crawls[0][2] == 'white':
        best = max(crawls, key=lambda c: c[3])
    else:
        best = min(crawls, key=lambda c: c[3])
    print(f'Playing {best[0]} for {best[2]}')
    engine.game.parse_move(best[0])
    print(engine.game)


def search_proc_2(move_queueu:Queue, store:EvalStore, node_registry:dict[str, MoveNode], active_workers:EvalManager.Value, keys:KeyChain):
    # Must rewrite using TreeNodeArgs!!!!!!
    while True:
        # logger.debug(f'Active workers: {active_workers.value}')
        with keys.get_counter():
            active_workers.value += 1
        print(f'Queue size {move_queueu.qsize()}')
        task = move_queueu.get()
        if task is None:
            break

        engine_copy = copy.deepcopy(task.engine)
        layer = task.layer
        # logger.debug(f'Search Proc 2 layer: {layer}')
        with keys.get_store():
            engine_copy.eval_store.update_evals(
                store.get_positions()
            )
        engine_copy.game.parse_move(task.move.chart.move, False, True)
        next_moves = engine_copy.find_ranked_moves()
        with keys.get_store():
            store.update_evals(
                engine_copy.eval_store.get_positions()
            )
        task.move.chart.set_next(
            next_moves[:engine_copy.breadth], layer, engine_copy.game.turn, engine_copy.game.fen
        )
        next_nodes = [
            set_movenode(mv) for mv in task.move.chart.next
        ]
        # logger.debug(f'')
        for n in next_nodes:
            # print(f'Processing node: {n.id} {n.chart}')
            task.move.next.append(n.id)
            with keys.get_registry():
                node_registry[n.id] = n

        # print(f'Task.move.next: {task.move.next}')
        with keys.get_registry():
            node_registry[task.move.id] = task.move
            # set parent node.next
            if task.parent_id is not None:
                parent = node_registry[task.parent_id]
                parent.next.append(task.move.id)
                node_registry[task.parent_id] = parent
        print(f'Layer {layer} is{' ' if layer>engine_copy.depth else  ' not'} greater than {engine_copy.depth}')

        if layer < engine_copy.depth:
            print(f'Adding new layer to the queue')
            next_searches = task.set_next(next_nodes, engine_copy)

            for s in next_searches:
                move_queueu.put(s)
        # logger.debug(f'Active workers: {active_workers.value}')
        
        move_queueu.task_done()
        with keys.get_counter():
            active_workers.value -= 1

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
    # EvalManager.register('KeyChain', KeyChain)
    with EvalManager() as manager:
        eval_store = manager.EvalStore()
        move_queue = manager.Queue()
        move_nodes = manager.dict()
        active_workers = manager.Value('i', 0)
        key_chain = KeyChain(manager)

        eval_store.set_positions(
            engine.eval_store.get_positions()
        )
        for mv in mv_args:
            move_queue.put(mv)

        processes = []
        for i in range(num_processes):
            p = Process(
                target=search_proc_2,
                args=(move_queue, eval_store, move_nodes, active_workers, key_chain),
                name=f'Worker-{i+1}'
            )
            processes.append(p)
            p.start()

        # print(f'Active workers: {active_workers.value}')

        while not move_queue.empty() and active_workers.value > 0:
            # logger.debug(f'Active workers: {active_workers.value}')
            time.sleep(0.01)

        for _ in range(num_processes):
            move_queue.put(None)

        for p in processes:
            p.join()

        engine.eval_store.update_evals(
            eval_store.get_positions()
        )
        
        # logger.info(f'Fast eval store: {engine.eval_store}')
        return build_tree(move_nodes, mv_nodes)

def build_tree(nodes:dict[str, MoveNode], root_nodes:list[MoveNode]) -> list[DepthChart]:
    results = []
    id_list = [node.id for node in root_nodes]
    # print(f'Node dict:')
    # for k,v in nodes.items():
    #     print(f'{k}: {v}, next: {v.next}')
    # print(f'Root nodes: {root_nodes}')
    # print(f'id_list: {id_list}')
    for id in id_list:
        node = nodes[id]
        # logger.debug(f'Current node: {node}')
        chart = node.chart
        # logger.debug(f'Next nodes: {[(i,nodes[i]) for i in node.next]}')
        chart.next = build_tree(nodes, [nodes[i] for i in node.next])
        results.append(chart)
    return results