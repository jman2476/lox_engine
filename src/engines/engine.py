from src.game import Game

class Engine():
    def __init__(self, game, side, name, depth):
        self.side = side
        self.game = game
        self.name = name
        self.depth = depth
        self.get_white = game.board.white
        self.get_black = game.board.black

    def __repr__(self):
        return f'{self.name} class engine playing {self.side}\nin game: {self.game}'
    
    def find_moves(self):
        ...

    def choose_move(self):
        ...

    def get_evaluation(self):
        ...