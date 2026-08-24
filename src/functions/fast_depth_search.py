from src.engines.fast_engine import FastEngine
from src.eval_store import EvalManager, EvalStore
from src.functions.depth_search import DepthChart, crawl_depth_chart
from multiprocessing import Process
from multiprocessing.managers import ValueProxy
import copy, time, random, os
from queue import Queue
from typing import Self
import logging
logger = logging.getLogger(__name__)


class SearchArgs():
    def __init__(self, engine:FastEngine, 
                 layer:int, parent:DepthChart, 
                 move:DepthChart, 
                 move_list:list[DepthChart] = []):
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
    def __init__(self, engine:FastEngine, 
                 layer: int, parent:str, 
                 move:MoveNode):
        self.engine = engine
        self.layer = layer
        self.parent_id = parent
        self.move = move

    def __repr__(self):
        return f'Layer {self.layer}, Parent: {self.parent_id}\nMove: {self.move}'


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

def depth_search(engine:FastEngine, num_workers:int=os.process_cpu_count()) -> list[DepthChart]:
    # Rewriting depth search tree to properly lock values
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
    if num_workers is None: num_workers = 4

    EvalManager.register('EvalStore', EvalStore)
    with EvalManager() as manager:
        eval_store = manager.EvalStore()
        move_queue = manager.Queue()
        move_nodes = manager.dict()
        count_procs = manager.Value('i', 0)
        print(f'count_procs is a {type(count_procs)} type')
        key_chain = KeyChain(manager)

        eval_store.set_positions(
            engine.eval_store.get_positions()
        )
        for mv in mv_args:
            count_procs.value += 1
            move_queue.put(mv)

        processes = []
        for i in range(num_workers):
            p = Process(
                target=search_process,
                args=(move_queue, eval_store, move_nodes, count_procs, key_chain),
                name=f'Worker-{i+1}'
            )
            processes.append(p)
            p.start()

        while not move_queue.empty() or count_procs.value > 0:
            print(f'Is queue empty: {move_queue.empty()}')
            print(f'Value of count_procs: {count_procs.value}')
            time.sleep(0.1)

        for _ in range(count_procs.value):
            move_queue.put(None)

        for p in processes:
            p.join()

        engine.eval_store.update_evals(
            eval_store.get_positions()
        )

        result_nodes = dict(move_nodes)
        print(f'Result nodes:')
        for rn in result_nodes:
            print(f'----------\n{rn}\n------------')

        return build_tree(move_nodes, mv_nodes)

def search_process(move_queue:Queue, store:EvalStore, 
                   registry:dict[str,MoveNode], 
                   counter, 
                   keys: KeyChain):
    while True:
        # with keys.counter:
        #     counter.value += 1
        task = move_queue.get()
        if task is None:
            break

        engine_copy = copy.deepcopy(task.engine)
        layer = task.layer
        logger.info(f'Processing on layer {layer}')
        with keys.get_store():
            engine_copy.eval_store.update_evals(
                store.get_positions()
            )

        engine_copy.game.parse_move(task.move.chart.move, False, True)
        next_moves = engine_copy.find_ranked_moves()
        task.move.chart.set_next(
            next_moves[:engine_copy.breadth], layer,
            engine_copy.game.turn, engine_copy.game.fen
        )
        next_nodes = [
            set_movenode(mv) for mv in task.move.chart.next
        ]
        with keys.store:
            store.update_evals(
                engine_copy.eval_store.get_positions()
            )

        with keys.registry:
            registry[task.move.id] = task.move

            if task.parent_id is not None:
                parent = registry[task.parent_id]
                parent.next.append(task.move.id)
                registry[task.parent_id] = parent

        if layer < engine_copy.depth:
            print(f'On layer {layer}, add next nodes')
            next_searches = task.set_next(next_nodes, engine_copy)

            for ns in next_searches:
                print(f'Adding node {ns} to queue')
                with keys.counter:
                    counter.value += 1
                move_queue.put(ns)
        else:
            print(f'Max depth search reached at layer {layer}')

        with keys.counter:
            counter.value -= 1
        move_queue.task_done()
            

def get_best_move(engine:FastEngine):
    move_tree = depth_search(engine)
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
        logger.debug(f'On layer {layer} Next nodes: {[node.id for node in next_nodes]}')
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
                print(f'Search {s} added to queue')
        else:
            print('Max depth reached')
            logger.debug('max depth reached')
        # logger.debug(f'Active workers: {active_workers.value}')
        
        with keys.get_counter():
            active_workers.value -= 1
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
    # EvalManager.register('KeyChain', KeyChain)
    with EvalManager() as manager:
        eval_store = manager.EvalStore()
        move_queue = manager.Queue()
        move_nodes = manager.dict()
        active_workers = manager.Value('i', 0)
        print(f'active workers is a {type(active_workers)} type')
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