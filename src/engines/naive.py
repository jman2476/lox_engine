from src.engines.engine import Engine
from src.game import Game
from src.functions.find_moves import find_move_notation
from src.functions.evaluation import get_evaluation
import copy

class NaiveEngine(Engine):
    def __init__(self, game:Game, side:str, depth:int=4):
        super().__init__(game, side, 'naive', depth)
        self.move_map = {}

    def find_moves(self, game=None):
        if game is None: # necessary to anayze moves at depth
            game = self.game
        moves = []
        self.white = self.game.board.white()
        self.black = self.game.board.black()
        pieces = self.white if game.turn == 'white' else self.black
        for piece in pieces:
            moves.extend(find_move_notation(self.game, piece))
        # Debugging: print moves w/ notation
        # print(f'Available engine moves: {moves}')
        return moves
    
    def choose_move(self):
        top_moves = {}
        available = self.evaluate_moves(self.find_moves())
        if available is None:
            print('No available moves')
            return
        ranked_moves = sorted(available, key=self.__eval_from_tuple__, reverse=True)
        print(f'Ranked engine moves for {self.game.turn}: {ranked_moves[:10]}')
        

    def evaluate_moves(self, move_list:list[str]) -> list[tuple[str, float]]:
        move_evaluation = []
        for move in move_list:
            eval = 0
            game_copy = copy.deepcopy(self.game)
            game_copy.parse_move(move)
            match game_copy.winner:
                case '1-0':
                    eval = 1000.0
                case '0-1':
                    eval = -1000.0
                case '1/2-1/2':
                    eval = 0.0
                case _:
                    eval = get_evaluation(game_copy.board)
            move_evaluation.append((move, eval))
        return move_evaluation
            
    def __eval_from_tuple__(self, tuple:tuple[str,float]) -> float:
        return tuple[1]