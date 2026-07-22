import unittest
from src.engines.naive import NaiveEngine
from src.functions.depth_search import (
    depth_search, DepthChart,
    crawl_depth_chart
    )
from src.game import Game
import time

class TestDepthSearch(unittest.TestCase):
    def test_depth_search(self):
        
        game = Game()
        game.start_new_game()
        engine = NaiveEngine(game, 'white', 5)
        start = time.perf_counter()
        move_charts = depth_search(engine=engine, depth=3, level=0, multi_proc=True)
        end = time.perf_counter()
        print(move_charts)
        print(f'Depth search time taken: {end-start}s')

        start = time.perf_counter()
        for ch in move_charts:
            print(crawl_depth_chart(ch))
        end = time.perf_counter()
        print(f'Crawl time taken: {end-start}s')

        self.assertTrue(isinstance(move_charts[0], DepthChart))
