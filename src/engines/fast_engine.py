from src.engines.engine import Engine
from src.functions.evaluation import get_evaluation
from src.functions.find_moves import find_move_notation
from src.game import Game
from typing import Literal
from src.eval_store import EvalStore, EvalManager
import copy, logging, time
from multiprocessing import Process, current_process

logger = logging.getLogger(__name__)

class FastEngine(Engine):
    def __init__(self, game:Game, 
                 side:Literal['white', 'black'], 
                 search:tuple[int,int]=(5,2)):
        super().__init__(game, side, 'fast', search[0])
        self.breadth = search[1]
        self.search = search
        self.eval_store = EvalStore()

    def find_ranked_moves(self) -> list[tuple[str, float]]:
        start = time.perf_counter()
        moves = self.find_moves()
        evaluations = self.eval_moves(moves)
        end = time.perf_counter()
        # logger.info(f'{current_process().name} FE.find_ranked_moves: {end-start}s')
        return self.rank_moves(evaluations)[:self.breadth]

    def find_moves(self) -> list[str]:
        start = time.perf_counter()
        self.white = self.game.board.white()
        self.black = self.game.board.black()
        pieces = self.white if self.game.turn == 'white' else self.black
        moves = []
        for p in pieces:
            moves.extend(find_move_notation(self.game, p))
        # print(f'Fast engine moves: {moves}')
        end = time.perf_counter()
        # logger.info(f'{current_process().name} FE.find_moves: {end-start}s')

        return moves

    def rank_moves(self, eval_moves:list[tuple[str,float]]
                   ) -> list[tuple[str,float]]:
        # rank moves decreasing for white's turn,
        #   decreasing for black's turn
        start = time.perf_counter()
        if len(eval_moves) == 0:
            print('No available moves')
            return []
        ranked = (sorted(eval_moves,
                        key=lambda x: x[1], reverse=True)
                if self.game.turn == 'white' else
                sorted(eval_moves,
                       key=lambda x: x[1], reverse=False))
        end = time.perf_counter()
        # logger.info(f'{current_process().name} FE.rank_moves: {end-start}s')
        return ranked[:10]

    def eval_moves(self, moves:list[str]
                    ) -> list[tuple[str, float]]:
        start = time.perf_counter()
        move_evals = []
        for mv in moves:
            eval = 0
            game_copy = copy.deepcopy(self.game)
            try:
                game_copy.parse_move(mv, False, True)
                stored_eval, exists = self.eval_store.get_eval(game_copy.fen)
                if exists:
                    eval = stored_eval
                    # logger.info('Move found in eval store')
                    
                else:
                    # logger.info('Move not found in eval store')
                    match game_copy.winner:
                        case '1-0':
                            eval = 1000.0
                        case '0-1':
                            eval = -1000.0
                        case '1/2-1/2':
                            eval = 0.0
                        case _:
                            eval = get_evaluation(game_copy.board)
                    self.eval_store.set_eval(game_copy.fen, eval)
                move_evals.append((mv, eval))
            except:
                print(f'Invalid move found: {mv}')
                continue
        end = time.perf_counter()
        # logger.info(f'{current_process().name} FE.eval_moves: {end-start}s')
        return move_evals
                
