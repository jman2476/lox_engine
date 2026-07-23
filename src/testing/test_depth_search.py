import unittest
from src.engines.naive import NaiveEngine
from src.functions.depth_search import (
    depth_search, DepthChart,
    crawl_depth_chart, 
    get_best_move
    )
from src.game import Game
import time

class TestDepthSearch(unittest.TestCase):
    def test_depth_search(self):
        print('------Depth Search Test------')
        game = Game()
        game.start_new_game()
        engine = NaiveEngine(game, 'white', 5)
        start = time.perf_counter()
        move_charts = depth_search(engine=engine, depth=3, level=0, multi_proc=True)
        end = time.perf_counter()
        print(move_charts)
        print(f'Depth search time taken: {end-start}s')

        side = move_charts[0].side
        best_move = None 
        start = time.perf_counter()
        for ch in move_charts:
            crawl = crawl_depth_chart(ch)
            print(crawl)
            if best_move is None:
                best_move = crawl
            elif best_move[4] > crawl[4] and side == 'white':
                best_move = ch
            elif best_move[4] < crawl[4] and side == 'black':
                best_move = ch
        end = time.perf_counter()
        print(f'Crawl time taken: {end-start}s')
        print(f'Best move: {best_move}')
        self.assertTrue(isinstance(move_charts[0], DepthChart))

    def test_depth_search_play_game(self):
        print('======Play game depth search======')
        game = Game()
        game.start_new_game()
        engine = NaiveEngine(game, 'white', 5)

        start = time.perf_counter()

        try:
            while game.winner is None:
                get_best_move(engine, 3, 5, False)
                print(game.board)
        except Exception as e:
            print(f'Exception found: {e}')
        finally:
            end = time.perf_counter()
            print(f'Game took {(end-start)/60} min')
        