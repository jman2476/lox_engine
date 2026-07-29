from typing import Self
from src.functions.depth_search import DepthChart

class MoveNode():
    def __init__(self, fen:str, turn:str, eval:float):
        self.fen = fen
        self.turn = turn
        self.eval = eval
        self.next:list[Self] = []

    def __repr__(self):
        return f'Position: {self.fen}\nTurn {self.turn}\nEvaluation: {self.eval}\nNext moves: {self.next}'

    def add_next(self, node:Self):
        self.next.append(node)

class MoveMap():
    def __init__(self):
        self.map:map[str:MoveNode] = {}

    def __repr__(self):
        for fen in self.map:
            return f'---{fen}---\n{self.map[fen]}'

    def add_node(self, node:MoveNode):
        self.map[node.fen] = node

    def parse_depth_chart(self, ch:DepthChart):
        if ch.fen in self.map:
            if ch.next != self.map[ch.fen].next:
                next_set = {*ch.next, *(self.map[ch.fen].next)}
                self.map[ch.fen].next = [MoveNode(ch.fen, ch.side, ch.eval) for mv in next_set]
        else:
            self.map[ch.fen] = MoveNode(ch.fen, ch.side, ch.eval)
        for mv in ch.next:
            self.parse_depth_chart(mv)