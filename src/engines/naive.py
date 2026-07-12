from src.engines.engine import Engine
from src.game import Game
from src.functions.find_moves import find_move_notation
from src.functions.evaluation import get_evaluation
import copy
import logging
from datetime import datetime
import random
from multiprocessing import Pool

logger = logging.getLogger('naive-engine-timing')
logging.basicConfig(filename='naive-engine.log', level=logging.INFO)

class NaiveEngine(Engine):
    def __init__(self, game:Game, side:str, depth:int=4):
        super().__init__(game, side, 'naive', depth)
        self.move_map = {}
        # loggerinfo('Naive engine instantiated')

    def find_moves(self, game=None):
        # logger.info(f'find_moves {self.game.turn} start {datetime.now()}')
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
        # logger.info(f'find_moves {self.game.turn} end {datetime.now()}')
        return moves
    
    def rank_moves(self):
        # logger.info(f'choose_move start {datetime.now()}')

        available = self.evaluate_moves(self.find_moves())
        if available is None:
            print('No available moves')
            # logger.info(f'choose_move escape {datetime.now()}')
            return []
        ranked_moves = (sorted(available, key=self.__eval_from_tuple__, reverse=True) 
                        if self.game.turn == 'white' else
                        sorted(available, key=self.__eval_from_tuple__, reverse=False))
        print(f'Ranked engine moves for {self.game.turn}: {ranked_moves[:10]}')
        # logger.info(f'choose_move end {datetime.now()}')
        if len(ranked_moves) > 10:
            return ranked_moves[:10]
        return ranked_moves 
    
    
    def rank_moves_process(self):
        # logger.info(f'choose_move start {datetime.now()}')
        moves = self.eval_moves_mp(self.find_moves())
        if moves is None:
            print('No available moves')
        ranked_moves = (sorted(moves, 
                               key=self.__eval_from_tuple__, reverse=True) 
                        if self.game.turn == 'white' else
                        sorted(moves, 
                               key=self.__eval_from_tuple__, reverse=False))
        print(f'Ranked engine moves for {self.game.turn}: {ranked_moves[:10]}')
        # logger.info(f'choose_move end {datetime.now()}')
        if len(ranked_moves) > 10:
            return ranked_moves[:10]
        return ranked_moves 
    

    def evaluate_moves(self, move_list:list[str]) -> list[tuple[str, float]]:
        # logger.info(f'evaluate_moves start {datetime.now()}')
        move_evaluation = []
        for move in move_list:
            # loggerinfo(f'evaluate_moves loop start {datetime.now()}')
            eval = 0
            game_copy = copy.deepcopy(self.game)
            try: 
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
            except:
                continue
        # loggerinfo(f'evaluate_moves end {datetime.now()}')
        return move_evaluation
            
    def __eval_from_tuple__(self, tuple:tuple[str,float]) -> float:
        return tuple[1]
    

    def eval_moves_mp(self, move_list:list[str]) -> list[tuple[str, float]]:
        # In future, may need to migrate to passing game state directly, and use starmap instead of imap
        logging.info(f'start eval moves mp for {self.game.turn}')
        move_evaluation = []
        pieces = self.white if self.game.turn == 'white' else self.black
        with Pool(self.set_threads(pieces)) as p:
            move_evaluation = list(p.imap_unordered(
                self.eval_move, move_list
            ))
            logging.debug(f'finished move_evaluation: {move_evaluation}')
        logging.debug(f'Leaving pool context')
        print('Evaluated moves:')
        print(f'{move_evaluation}')
        print('-----------------')
        return [m for m in move_evaluation if m is not None]


    def eval_move(self, move:str) -> tuple[str,float]:
        logging.info(f'start eval_move: {move}')
        eval = 0
        game_copy = copy.deepcopy(self.game)
        try: 
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
            logging.debug(f'finish eval move: {move} -> {eval}')
            return move, eval
        except:
            logging.debug(f'move {eval} fail eval_move')
            return 
    

    def play_best_move(self):
        # loggerinfo(f'play-best-move for {self.game.turn} start {datetime.now()}')
        moves = self.rank_moves()
        choice = None
        if len(moves) != 0:
            best_moves = [mv for mv in moves if mv[1] == moves[0][1]]
            choice = random.choice(best_moves)
            self.game.parse_move(choice[0])
        else:
            print('No moves found')
        # loggerinfo(f'play-best-move for {self.game.turn} end: {choice} {datetime.now()}')
        return choice


    def compare_rank_moves(self):
        # loggerinfo(f'Start compare_rank_moves:')
        # loggerinfo(f'Start rank_moves: {datetime.now()}')
        self.rank_moves()
        # loggerinfo(f'End rank_moves: {datetime.now()}')
        # loggerinfo(f'Start rank_moves_mp: {datetime.now()}')
        self.rank_moves_process()
        # loggerinfo(f'End rank_moves_mp: {datetime.now()}')

    def play_move_multi_proc(self):
        moves = self.rank_moves_process()
        choice = None
        if len(moves) != 0:
            best_moves = [m for m in moves 
                          if m[1] == moves[0][1]]
            choice = random.choice(best_moves)
            self.game.parse_move(choice[0])
        else:
            print('No moves found')
        return choice
        
    def set_threads(self, pieces):
        return len(pieces)