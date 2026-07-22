from src.engines.naive import NaiveEngine
from src.engines.engine import Engine
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
        base_str = f'[{self.move}, {self.eval}, {self.side}]:\n'
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

def depth_search(engine:Engine, depth:int=3, breadth:int=5, level:int=0, moves:list[DepthChart]=[]) -> list[DepthChart]:
    logger.info(f'Starting depth={depth} search: side {engine.game.turn} level {level}, moves: {moves}')
    if depth <= level: return moves
    if moves == []:
        logger.info('empty move list')
        move_list = get_ranked_moves(engine)
        logger.info(f'Had empty move list, new move list: {move_list}')
        for i, mv in enumerate(move_list):
            if i >= breadth: break
            moves.append(DepthChart(mv[0], mv[1], level, engine.game.turn))
    i = 0
    total = len(moves)
    for mv in moves:
        if level == 0:
            logger.info(f'Move {i} of {total}')
            i += 1
        engine_copy = copy.deepcopy(engine)
        engine_copy.game.parse_move(mv.move)
        ranked_moves = get_ranked_moves(engine_copy)
        if len(ranked_moves) < breadth:
            mv.set_next(ranked_moves, level, engine_copy.game.turn)
        else:
            mv.set_next(ranked_moves[:breadth], level, engine_copy.game.turn)
        depth_search(engine_copy, depth, breadth, level+1, mv.next)
    return moves



def get_ranked_moves(engine:Engine)->list[tuple[str, float]]:
    match engine:
        case NaiveEngine():
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
        