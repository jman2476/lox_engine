from src.game import Game
from src.engines.fast_engine import FastEngine
from src.functions.fast_depth_search import get_best_move
import cProfile
import multiprocessing as mp


def main():
    game = Game()
    game.start_new_game()
    engine = FastEngine(game, 'white', (2,3))

    cProfile.run('get_best_move(engine)')

if __name__ == '__main__':
    mp.set_start_method('forkserver')
    main()