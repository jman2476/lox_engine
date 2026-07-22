import unittest
from src.engines.naive import NaiveEngine
from src.functions.depth_search import (
    depth_search, DepthChart,
    crawl_depth_chart
    )
from src.game import Game

class TestDepthSearch(unittest.TestCase):
    def test_depth_search(self):
        game = Game()
        game.start_new_game()
        engine = NaiveEngine(game, 'white', 5)
        move_charts = depth_search(engine=engine, depth=5, level=0)
        print(move_charts)

        for ch in move_charts:
            print(crawl_depth_chart(ch))

        self.assertTrue(isinstance(move_charts[0], DepthChart))
