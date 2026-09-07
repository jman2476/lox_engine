from src.game import Game
from src.engines.fast_engine import FastEngine
from src.functions.fast_depth_search import get_best_move
import cProfile, pstats
import multiprocessing as mp


def main():
    game = Game()
    game.start_new_game()
    engine = FastEngine(game, 'white', (2,3))

    profiler = cProfile.Profile()
    profiler.enable()

    get_best_move(engine)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(30)

    stats.sort_stats('tottime')
    stats.print_stats(30)

if __name__ == '__main__':
    mp.set_start_method('forkserver')
    main()