import unittest
from src.move_map import MoveMap, MoveNode
from src.engines.naive import NaiveEngine
from src.functions.depth_search import (
    depth_search,
    get_best_move, get_best_move_mp,
    DepthChart
)
from src.game import Game

class TestMoveMap(unittest.TestCase):
    def test_movemap_crawlchart(self):
        game = Game()
        game.start_new_game()
        engine_w = NaiveEngine(game, 'white')
        engine_w.move_map = MoveMap()

        chart_list = depth_search(engine_w, 2, 3)
        print(f'Chart list len: {len(chart_list)}')
        for chart in chart_list:
            print(chart.move, chart.eval)
            engine_w.move_map.parse_depth_chart(chart)

        print(f'Move map:\n{engine_w.move_map}')

    