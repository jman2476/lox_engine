from src.engines.naive import NaiveEngine
from src.engines.engine import Engine
import copy


class DepthChart():
    def __init__(self, move:str, eval:float):
        self.move = move
        self.eval = eval
        self.next:list[DepthChart] = []

    def set_next(self, moves:list[tuple[str,float]]):
        for mv in moves:
            depth_node = DepthChart(mv[0], mv[1])
            self.next.append(depth_node)

def depth_search(engine:Engine, depth:int=3, breadth:int=5, level:int=0, moves:list[DepthChart]=[]) -> list[DepthChart]:
    if depth <= level: return moves
    if moves == []:
        move_list = get_ranked_moves(engine)
        for i, mv in enumerate(move_list):
            if i >= breadth: break
            moves.append(DepthChart(mv[0], mv[1]))
    for mv in move_list:
        engine_copy = copy.deepcopy(engine)
        engine_copy.game.parse_move(mv.move)
        ranked_moves = get_ranked_moves(engine_copy)
        if len(ranked_moves) < breadth:
            mv.set_next(ranked_moves)
        else:
            mv.set_next(ranked_moves[:breadth])
        depth_search(engine_copy, depth, breadth, level+1, mv.next)
    return moves



def get_ranked_moves(engine:Engine)->list[tuple[str, float]]:
    match engine:
        case NaiveEngine():
            return engine.rank_moves()
        case _:
            raise TypeError('Depth search: Unknown engine type')