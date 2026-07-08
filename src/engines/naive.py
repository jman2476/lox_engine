from src.engines.engine import Engine
from src.game import Game
from src.functions.find_moves import find_move_notation
from src.functions.evaluation import get_evaluation
import copy
import logging
from datetime import datetime
import random

logger = logging.getLogger('naive-engine-timing')
logging.basicConfig(filename='naive-engine.log', level=logging.INFO)

class NaiveEngine(Engine):
    def __init__(self, game:Game, side:str, depth:int=4):
        super().__init__(game, side, 'naive', depth)
        self.move_map = {}
        logger.info('Naive engine instantiated')

    def find_moves(self, game=None):
        logger.info(f'find_moves {self.game.turn} start {datetime.now()}')
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
        logger.info(f'find_moves {self.game.turn} end {datetime.now()}')
        return moves
    
    def rank_moves(self):
        logger.info(f'choose_move start {datetime.now()}')

        available = self.evaluate_moves(self.find_moves())
        if available is None:
            print('No available moves')
            logger.info(f'choose_move escape {datetime.now()}')
            return []
        ranked_moves = (sorted(available, key=self.__eval_from_tuple__, reverse=True) 
                        if self.game.turn == 'white' else
                        sorted(available, key=self.__eval_from_tuple__, reverse=False))
        print(f'Ranked engine moves for {self.game.turn}: {ranked_moves[:10]}')
        logger.info(f'choose_move end {datetime.now()}')
        if len(ranked_moves) > 10:
            return ranked_moves[:10]
        return ranked_moves 

    def evaluate_moves(self, move_list:list[str]) -> list[tuple[str, float]]:
        logger.info(f'evaluate_moves start {datetime.now()}')
        move_evaluation = []
        for move in move_list:
            logger.info(f'evaluate_moves loop start {datetime.now()}')
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
        logger.info(f'evaluate_moves end {datetime.now()}')
        return move_evaluation
            
    def __eval_from_tuple__(self, tuple:tuple[str,float]) -> float:
        return tuple[1]
    
    def play_best_move(self):
        logger.info(f'play-best-move for {self.game.turn} start {datetime.now()}')
        moves = self.rank_moves()
        choice = None
        if len(moves) != 0:
            best_moves = [mv for mv in moves if mv[1] == moves[0][1]]
            choice = random.choice(best_moves)
            self.game.parse_move(choice[0])
        else:
            print('No moves found')
        logger.info(f'play-best-move for {self.game.turn} end: {choice} {datetime.now()}')
