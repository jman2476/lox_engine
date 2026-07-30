from typing import Self
from src.functions.depth_search import DepthChart

class MoveNode():
    def __init__(self, fen:str, turn:str, eval:float):
        self.fen = fen.split()[0]
        self.turn = turn
        self.eval = eval
        self.next:list[Self] = []

    def __repr__(self):
        return f'Position: {self.fen}\nTurn {self.turn}\nEvaluation: {self.eval}\nNext moves: \n{self.next}\n'

    def add_next(self, node:Self):
        self.next.append(node)

class MoveMap():
    def __init__(self):
        self.map:map[str:MoveNode] = {}

    def __repr__(self):
        map_str = ''
        for fen in self.map:
            map_str += f'---{fen}---\n{self.map[fen]}\n'
        return map_str

    def add_node(self, dc:DepthChart):
        self.map[dc.fen] = MoveNode(dc.fen, dc.side, dc.eval)
        return self.map[dc.fen]

    def parse_depth_chart(self, ch:DepthChart) -> MoveNode:
        if ch.fen not in self.map:
            current = self.add_node(ch)
        else:
            current = self.map[ch.fen]
        for mv in ch.next:
            next = self.parse_depth_chart(mv)
            if next not in current.next:
                current.next.append(next)
        return current