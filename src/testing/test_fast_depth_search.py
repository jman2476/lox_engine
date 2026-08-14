import unittest
from src.functions.fast_depth_search import (depth_search, 
                                            search_process,
                                            get_best_move)
from src.engines.fast_engine import FastEngine
from src.game import Game

class TestFastDepthSearch(unittest.TestCase):
    def test_depth_search(self):
        game = Game()
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))

        results = depth_search(engine)
        print(results)