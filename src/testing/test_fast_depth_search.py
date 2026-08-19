import unittest
from src.functions.fast_depth_search import (depth_search, 
                                            search_process,
                                            get_best_move,
                                            depth_search_tree)
from src.engines.fast_engine import FastEngine
from src.game import Game
import time

class TestFastDepthSearch(unittest.TestCase):
    # def test_depth_search(self):
    #     print('------Fast Depth Search------')
    #     game = Game()
    #     game.start_new_game()
    #     engine = FastEngine(game, 'white', (2,3))

    #     start = time.perf_counter()
    #     results = depth_search(engine)
    #     end = time.perf_counter()
    #     print(f'DS results: {results}')
    #     print(f'Elapsed time: {end - start}s')

    def test_depth_search_tree(self):
        print('------Fast Depth Search Tree-------')
        game = Game()
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))

        start = time.perf_counter()
        results = depth_search_tree(engine)
        end = time.perf_counter()
        print(f"DST results: \n{results}")
        print(f'Elapsed time: {end - start}s')

    def test_get_play_best_move(self):
        print('------Get/Play Best Move-------')
        game = Game()
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))

        start = time.perf_counter()
        get_best_move(engine)
        end = time.perf_counter()
        print(f'FDS time: {end - start}s')