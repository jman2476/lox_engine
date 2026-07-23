from src.engines.naive import NaiveEngine
from src.engines.engine import Engine
from multiprocessing import Pool
import copy
import logging
logger = logging.getLogger(__name__)

class DepthChart():
    def __init__(self, move:str, eval:float, level:int, side:str):
        self.move = move
        self.eval = eval
        self.level = level
        self.side = side
        self.next:list[DepthChart] = []

    def __repr__(self):
        base_str = f'[{self.move}, {self.eval}, {self.side}, {self.level}]:\n'
        for node in self.next:
            node_str = f'-{node}'
            for i in range(node.level):
                node_str = '    ' + node_str
            base_str += node_str
        return base_str

    def set_next(self, moves:list[tuple[str,float]], prev_level:int, side:str):
        for mv in moves:
            depth_node = DepthChart(mv[0], mv[1], prev_level + 1, side)
            self.next.append(depth_node)

def depth_search(engine:Engine, depth:int=3, breadth:int=5, level:int=0, moves:list[DepthChart]=[], multi_proc:bool=False) -> list[DepthChart]:
    logger.info(f'Starting depth={depth} search: side {engine.game.turn} level {level}, moves: {moves}')
    if depth <= level: return moves
    if moves == []:
        logger.info('empty move list')
        move_list = get_ranked_moves(engine, multi_proc)
        logger.info(f'Had empty move list, new move list: {move_list}')
        for i, mv in enumerate(move_list):
            if i >= breadth: break
            moves.append(DepthChart(mv[0], mv[1], level, engine.game.turn))
    i = 1
    total = len(moves)
    for mv in moves:
        if level == 0:
            logger.info(f'Move {i} of {total}')
            i += 1
        engine_copy = copy.deepcopy(engine)
        engine_copy.game.parse_move(mv.move)
        ranked_moves = get_ranked_moves(engine_copy, multi_proc)
        if len(ranked_moves) < breadth:
            mv.set_next(ranked_moves, level, engine_copy.game.turn)
        else:
            mv.set_next(ranked_moves[:breadth], level, engine_copy.game.turn)
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
            moves.append(DepthChart(mv[0], mv[1], level, engine.game.turn))

    move_args = [(engine, mv, depth, breadth, 
                  level, multi_proc) for mv in moves]

    with Pool() as p:
        new_moves = list(p.imap_unordered(
            search_process, move_args
        ))
    # for mv in moves:
    #     if level == 0:
    #         logger.info(f'Move {i} of {total}')
    #         i += 1
    #     engine_copy = copy.deepcopy(engine)
    #     engine_copy.game.parse_move(mv.move)
    #     ranked_moves = get_ranked_moves(engine_copy, multi_proc)
    #     if len(ranked_moves) < breadth:
    #         mv.set_next(ranked_moves, level, engine_copy.game.turn)
    #     else:
    #         mv.set_next(ranked_moves[:breadth], level, engine_copy.game.turn)
    #     depth_search(engine_copy, depth, breadth, level+1, mv.next)
    return new_moves


def search_process(engine:Engine, mv:DepthChart, depth:int, breadth:int, level:int, multi_proc:bool):
    engine_copy = copy.deepcopy(engine)
    engine_copy.game.parse_move(mv.move)
    ranked_moves = get_ranked_moves(engine_copy, multi_proc)
    if len(ranked_moves) < breadth:
        mv.set_next(ranked_moves, level, engine_copy.game.turn)
    else:
        mv.set_next(ranked_moves[:breadth], level, engine_copy.game.turn)
    depth_search(engine_copy, depth, breadth, level+1, mv.next)
    return mv


def get_ranked_moves(engine:Engine, multi_proc:bool=False)->list[tuple[str, float]]:
    match engine:
        case NaiveEngine():
            if multi_proc:
                engine.rank_moves_process()
            return engine.rank_moves()
        case _:
            raise TypeError('Depth search: Unknown engine type')


# return format: [move, eval, side, best final eval, final move side]
def crawl_depth_chart(chart:DepthChart) -> list[str, float, str, float, str]: 
    result = [chart.move, chart.eval, chart.side, None, None]
    if len(chart.next) == 0:
        return chart.move, chart.eval, chart.side, None, None

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
    best_move = None 
    for ch in move_charts:
        crawl = crawl_depth_chart(ch)
        print('crawl', crawl)
        if best_move is None:
            best_move = crawl
        elif best_move[4] > crawl[4] and engine.game.turn == 'white':
            best_move = ch
        elif best_move[4] < crawl[4] and engine.game.turn == 'black':
            best_move = ch

    print(f'Playing {best_move[0]} for {engine.game.turn}')
    engine.game.parse_move(best_move[0])