from typing import Self

class MoveNode():
    def __init__(self, fen:str, eval:float):
        self.fen = fen
        self.eval = eval
        self.next:list[Self] = []

    def add_next(self, node:Self):
        self.next.append(node)

class MoveMap():
    def __init__(self):
        self.map:map[str:MoveNode] = {}

    def add_node(self, node:MoveNode):
        self.map[node.fen] = node

