from src.engines.naive import NaiveEngine
from src.engines.engine import Engine
from multiprocessing import Pool, Manager
import copy
import logging
logger = logging.getLogger(__name__)

class DepthChart():
    def __init__(self, move:str, eval:float, level:int, side:str, fen:str):
        self.move = move
        self.eval = eval
        self.level = level
        self.side = side
        self.next:list[DepthChart] = []
        self.fen = fen

    def __repr__(self):
        base_str = f'[{self.move}, {self.eval}, {self.side}, {self.level}]:\n'
        for node in self.next:
            node_str = f'-{node}'
            for i in range(node.level):
                node_str = '    ' + node_str
            base_str += node_str
        return base_str

    def set_next(self, moves:list[tuple[str,float]], prev_level:int, side:str, fen:str):
        for mv in moves:
            depth_node = DepthChart(mv[0], mv[1], prev_level + 1, side, fen)
            self.next.append(depth_node)

def depth_search(engine:Engine, depth:int=3, breadth:int=5, level:int=0, moves:list[DepthChart]=[], multi_proc:bool=False, eval_dict:dict[str,float] = {}) -> list[DepthChart]:
    logger.info(f'Starting depth={depth} search: side {engine.game.turn} level {level}, moves: {moves}')
    if depth <= level: return moves
    if moves == []:
        logger.info('empty move list')
        move_list = get_ranked_moves(engine, multi_proc)
        logger.info(f'Had empty move list, new move list: {move_list}')
        for i, mv in enumerate(move_list):
            if i >= breadth: break
            moves.append(DepthChart(mv[0], mv[1], level, engine.game.turn, engine.game.fen))
    i = 1
    total = len(moves)
    for mv in moves:
        if level == 0:
            logger.info(f'Move {i} of {total}')
            i += 1
        engine_copy = copy.deepcopy(engine)
        engine_copy.game.parse_move(mv.move, False, True)
        ranked_moves = get_ranked_moves(engine_copy, multi_proc)
        if len(ranked_moves) < breadth:
            mv.set_next(ranked_moves, level, engine_copy.game.turn, engine_copy.game.fen)
        else:
            mv.set_next(ranked_moves[:breadth], level, engine_copy.game.turn, engine_copy.game.fen)
        depth_search(engine_copy, depth, breadth, level+1, mv.next)
    return moves

# Alter this to us multiprocessing
def depth_search_multiprocess(engine:Engine, depth:int=3, breadth:int=5, level:int=0, moves:list[DepthChart]=[], multi_proc:bool=False) -> list[DepthChart]:
    logger.info(f'Starting depth={depth} search: side {engine.game.turn} level {level}, moves: {moves}')
    if depth <= level: return moves
    if moves == []:
        logger.info('empty move list')
        move_list = get_ranked_moves(engine, multi_proc)
        logger.info(f'Had empty move list, new move list: {move_list}')
        for i, mv in enumerate(move_list):
            if i >= breadth: break
            moves.append(DepthChart(mv[0], mv[1], level, engine.game.turn, engine.game.fen))

    with Manager() as manager:
        eval_dict = manager.dict()
        eval_dict.update(engine.eval_dict)

        move_args = [(engine, mv, depth, breadth, 
                    level, multi_proc, eval_dict) for mv in moves]

        with Pool() as p:
            new_moves = list(p.starmap(
                search_process, move_args
            ))

        engine.eval_dict.update(eval_dict)
    return new_moves


def search_process(engine:Engine, mv:DepthChart, depth:int, breadth:int, level:int, multi_proc:bool, eval_dict:dict[str,float] = {}):
    engine_copy = copy.deepcopy(engine)
    engine_copy.game.parse_move(mv.move, False, True)
    engine_copy.eval_dict.update(eval_dict)
    ranked_moves = get_ranked_moves(engine_copy, multi_proc)
    if len(ranked_moves) < breadth:
        mv.set_next(ranked_moves, level, engine_copy.game.turn, engine_copy.game.fen)
    else:
        mv.set_next(ranked_moves[:breadth], level, engine_copy.game.turn, engine_copy.game.fen)
    depth_search(engine_copy, depth, breadth, level+1, mv.next)
    eval_dict.update(engine_copy.eval_dict)
    return mv


def get_ranked_moves(engine:Engine, multi_proc:bool=False)->list[tuple[str, float]]:
    match engine:
        case NaiveEngine():
            if multi_proc:
                return engine.rank_moves_process()
            return engine.rank_moves()
        case _:
            raise TypeError('Depth search: Unknown engine type')


# return format: [move, eval, side, best final eval, final move side]
def crawl_depth_chart(chart:DepthChart) -> list[str, float, str, float, str]: 
    result = [chart.move, chart.eval, chart.side, None, None]
    if len(chart.next) == 0:
        return [chart.move, chart.eval, chart.side, None, None]

    for mv in chart.next:
        mv_crawl = crawl_depth_chart(mv)
        if mv_crawl[3] is None:
            if result[3] is None:
                result[3] = mv_crawl[1]
                result[4] = mv_crawl[2]
            elif mv_crawl[2] == 'white':
                result[4] = mv_crawl[2]
                result[3] = max(mv_crawl[1], result[3])
            elif mv_crawl[2] == 'black':
                result[4] = mv_crawl[2]
                result[3] = min(mv_crawl[1], result[3])
            else:
                raise ValueError(f'Bad move side: listed as {mv_crawl[2]}')
        else:
            if result[3] is None:
                result[3] = mv_crawl[3]
                result[4] = mv_crawl[4]
            elif result[4] == 'white':
                result[3] = max(mv_crawl[3], result[3])
            else:
                result[3] = min(mv_crawl[3], result[3])

    return result


def get_best_move(engine:Engine, depth:int, breadth:int, multiproc:bool=False):
    move_charts = depth_search(engine, depth, breadth, moves=[], multi_proc=multiproc)
    crawls = []
    for ch in move_charts:
        crawl = crawl_depth_chart(ch)
        print('crawl', crawl)
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

def get_best_move_mp(engine:Engine, depth:int, breadth:int, multiproc:bool=False):
    move_charts = depth_search_multiprocess(engine, depth, breadth, moves=[], multi_proc=multiproc)
    crawls = []
    for ch in move_charts:
        crawl = crawl_depth_chart(ch)
        print('crawl', crawl)
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
    logger.debug(f'Naive Engine eval dict: {engine.eval_dict}')