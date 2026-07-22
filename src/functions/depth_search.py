from src.engines.naive import NaiveEngine
from src.engines.engine import Engine


class DepthChart():
    def __init__(self, move:str, eval:float):
        self.move = move
        self.eval = eval
        self.next:list[DepthChart] = []

    def set_next(self, moves:list[tuple[str,float]]):
        for mv in moves:
            depth_node = DepthChart(mv[0], mv[1])
            self.next.append(depth_node)

def depth_search(engine:Engine, depth:int=3, moves:list[str]=[]) -> DepthChart:
    ...