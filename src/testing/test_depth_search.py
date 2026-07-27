import unittest
from src.engines.naive import NaiveEngine
from src.functions.depth_search import (
    depth_search, depth_search_multiprocess, DepthChart,
    crawl_depth_chart, 
    get_best_move
    )
from src.game import Game
import time
import multiprocessing as mp

class TestDepthSearch(unittest.TestCase):
    # def test_depth_search_fork(self):
    #     if __name__ == 'src.testing.test_depth_search':
    #         mp.set_start_method('fork')
            
    #         print('------Depth Search Test Fork------')
    #         game = Game()
    #         game.start_new_game()
    #         engine = NaiveEngine(game, 'white', 5)
    #         start = time.perf_counter()
    #         move_charts = depth_search(engine=engine, depth=3, level=0, multi_proc=True)
    #         end = time.perf_counter()
    #         # print(move_charts)
    #         print(f'Depth search time taken: {end-start}s')

    #         side = move_charts[0].side
    #         best_move = None 
    #         start = time.perf_counter()
    #         for ch in move_charts:
    #             crawl = crawl_depth_chart(ch)
    #             # print(crawl)
    #             if best_move is None:
    #                 best_move = crawl
    #             elif best_move[4] > crawl[4] and side == 'white':
    #                 best_move = ch
    #             elif best_move[4] < crawl[4] and side == 'black':
    #                 best_move = ch
    #         end = time.perf_counter()
    #         print(f'Crawl time taken: {end-start}s')
    #         print(f'Best move: {best_move}')
    #         self.assertTrue(isinstance(move_charts[0], DepthChart))


    # def test_depth_search_single(self):
    #     print('------Depth Search Test Single Process------')
    #     game = Game()
    #     game.start_new_game()
    #     engine = NaiveEngine(game, 'white', 5)
    #     start = time.perf_counter()
    #     move_charts = depth_search(engine=engine, depth=3, level=0, multi_proc=False)
    #     end = time.perf_counter()
    #     # print(move_charts)
    #     print(f'Depth search time taken: {end-start}s')

    #     side = move_charts[0].side
    #     best_move = None 
    #     start = time.perf_counter()
    #     for ch in move_charts:
    #         crawl = crawl_depth_chart(ch)
    #         # print(crawl)
    #         if best_move is None:
    #             best_move = crawl
    #         elif best_move[4] > crawl[4] and side == 'white':
    #             best_move = ch
    #         elif best_move[4] < crawl[4] and side == 'black':
    #             best_move = ch
    #     end = time.perf_counter()
    #     print(f'Crawl time taken: {end-start}s')
    #     print(f'Best move: {best_move}')
    #     self.assertTrue(isinstance(move_charts[0], DepthChart))

    # def test_depth_search_spawn(self):
    #         if __name__ == 'src.testing.test_depth_search':
    #             mp.set_start_method('spawn')
                
    #             print('------Depth Search Test Spawn------')
    #             game = Game()
    #             game.start_new_game()
    #             engine = NaiveEngine(game, 'white', 5)
    #             start = time.perf_counter()
    #             move_charts = depth_search(engine=engine, depth=3, level=0, multi_proc=True)
    #             end = time.perf_counter()
    #             # print(move_charts)
    #             print(f'Depth search time taken: {end-start}s')
    
    #             side = move_charts[0].side
    #             best_move = None 
    #             start = time.perf_counter()
    #             for ch in move_charts:
    #                 crawl = crawl_depth_chart(ch)
    #                 # print(crawl)
    #                 if best_move is None:
    #                     best_move = crawl
    #                 elif best_move[4] > crawl[4] and side == 'white':
    #                     best_move = ch
    #                 elif best_move[4] < crawl[4] and side == 'black':
    #                     best_move = ch
    #             end = time.perf_counter()
    #             print(f'Crawl time taken: {end-start}s')
    #             print(f'Best move: {best_move}')
    #             self.assertTrue(isinstance(move_charts[0], DepthChart))
    

    def test_depth_search_forkserver(self):
            print(__name__)
            print(__name__ == 'src.testing.test_depth_search')
            if __name__ == 'src.testing.test_depth_search':
                mp.set_start_method('forkserver')
                print('------Depth Search Test Fork Server------')
                game = Game()
                game.start_new_game()
                engine = NaiveEngine(game, 'white', 5)
                start = time.perf_counter()
                move_charts = depth_search(engine=engine, depth=3, level=0, multi_proc=True)
                end = time.perf_counter()
                # print(move_charts)
                print(f'Depth search time taken: {end-start}s')
    
                side = move_charts[0].side
                best_move = None 
                start = time.perf_counter()
                for ch in move_charts:
                    crawl = crawl_depth_chart(ch)
                    # print(crawl)
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

    def test_depth_search_mp_forkserver(self):
        print(__name__)
        print(__name__ == 'src.testing.test_depth_search')
        if __name__ == 'src.testing.test_depth_search':
            # mp.set_start_method('forkserver')
            print('------Depth Search MP Test Fork Server------')
            game = Game()
            game.start_new_game()
            engine = NaiveEngine(game, 'white', 5)
            start = time.perf_counter()
            move_charts = depth_search_multiprocess(engine=engine, depth=3, level=0, multi_proc=False)
            end = time.perf_counter()
            # print(move_charts)
            print(f'Depth search time taken: {end-start}s')

            side = move_charts[0].side
            best_move = None 
            start = time.perf_counter()
            for ch in move_charts:
                crawl = crawl_depth_chart(ch)
                # print(crawl)
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


    # def test_depth_search_play_game(self):
    #     print('======Play game depth search======')
    #     game = Game()
    #     game.start_new_game()
    #     engine_w = NaiveEngine(game, 'white', 5)
    #     engine_b = NaiveEngine(game, 'black', 5)

    #     start = time.perf_counter()
#     try:
    #         while game.winner is None:
    #             print(f'Premove board: {game.turn}\'s turn\n',game.board)
    #             print(f'White\'s board: {engine_w.game.turn}\'s turn\n{engine_w.game.board}')
    #             print(f'Black\'s board: {engine_b.game.turn}\'s turn\n{engine_b.game.board}')
    #             match game.turn:
    #                 case 'white':
    #                     get_best_move(engine_w, 3, 5, False)
    #                 case 'black':
    #                     get_best_move(engine_b, 3, 5, False)
    #             print('Postmove board: \n',game.board)
    #     except Exception as e:
    #         print(f'Exception found: {e}')
    #     finally:
    #         end = time.perf_counter()
    #         print(f'Game took {(end-start)/60} min')
        
    # def test_eval_mating_pos(self):
    #     print('-----Test: Mate in 1-----')
    #     game = Game()
    #     game.read_fen('8/8/8/5Q2/2R5/6k1/8/7K w - - 47 103')
    #     engine = NaiveEngine(game, 'white', 5)
    #     start = time.perf_counter()
    #     move_charts = depth_search(engine=engine, depth=3, level=0, multi_proc=True)
    #     end = time.perf_counter()
    #     print(move_charts)
    #     print(f'Depth search time taken: {end-start}s')

    #     side = move_charts[0].side
    #     best_move = None 
    #     start = time.perf_counter()
    #     for ch in move_charts:
    #         crawl = crawl_depth_chart(ch)
    #         print(crawl)
    #         if best_move is None:
    #             best_move = crawl
    #         elif best_move[4] < crawl[4] and side == 'white':
    #             best_move = crawl
    #         elif best_move[4] > crawl[4] and side == 'black':
    #             best_move = crawl
    #     end = time.perf_counter()
    #     print(f'Crawl time taken: {end-start}s')
    #     print(f'Best move: {best_move}')
    #     self.assertTrue(isinstance(move_charts[0], DepthChart))

    # def test_depth_search_m2(self):
    #     print('======Play M2 position depth search======')
    #     game = Game()
    #     game.read_fen('8/8/8/5Q2/2R5/6k1/8/7K w - - 47 103')
    #     engine_w = NaiveEngine(game, 'white', 5)
    #     engine_b = NaiveEngine(game, 'black', 5)

    #     start = time.perf_counter()
    #     try:
    #         while game.winner is None:
    #             print(f'Premove board: {game.turn}\'s turn\n',game.board)
    #             print(f'White\'s board: {engine_w.game.turn}\'s turn\n{engine_w.game.board}')
    #             print(f'Black\'s board: {engine_b.game.turn}\'s turn\n{engine_b.game.board}')
    #             match game.turn:
    #                 case 'white':
    #                     get_best_move(engine_w, 3, 5, False)
    #                 case 'black':
    #                     get_best_move(engine_b, 3, 5, False)
    #             print('Postmove board: \n',game.board)
    #     except Exception as e:
    #         print(f'Exception found: {e}')
    #     finally:
    #         end = time.perf_counter()
    #         print(f'Game took {(end-start)/60} min')

    # def test_depth_search_m2(self):
    #     print('======Play -M1 position depth search======')
    #     game = Game()
    #     game.read_fen('6r1/ppp2k1p/8/4p3/3nP3/5P2/PPPP1P1P/RNB1K1R1 b Q - 2 13')
    #     engine_w = NaiveEngine(game, 'white', 5)
    #     engine_b = NaiveEngine(game, 'black', 5)

    #     start = time.perf_counter()
    #     try:
    #         while game.winner is None:
    #             print(f'Premove board: {game.turn}\'s turn\n',game.board)
    #             print(f'White\'s board: {engine_w.game.turn}\'s turn\n{engine_w.game.board}')
    #             print(f'Black\'s board: {engine_b.game.turn}\'s turn\n{engine_b.game.board}')
    #             match game.turn:
    #                 case 'white':
    #                     get_best_move(engine_w, 3, 5, False)
    #                 case 'black':
    #                     get_best_move(engine_b, 3, 5, False)
    #             print('Postmove board: \n',game.board)
    #     except Exception as e:
    #         print(f'Exception found: {e}')
    #     finally:
    #         end = time.perf_counter()
    #         print(f'Game took {(end-start)/60} min')
            

    # def test_depth_search_m5(self):
    #     print('======Play M5 position depth search======')
    #     game = Game()
    #     game.read_fen('6k1/R7/8/2P5/4P3/6P1/P4P2/6K1 w - - 1 32')
    #     engine_w = NaiveEngine(game, 'white', 5)
    #     engine_b = NaiveEngine(game, 'black', 5)

    #     start = time.perf_counter()
    #     try:
    #         while game.winner is None:
    #             print(f'Premove board: {game.turn}\'s turn\n',game.board)
    #             print(game)
    #             # print(f'White\'s board: {engine_w.game.turn}\'s turn\n{engine_w.game.board}')
    #             # print(f'Black\'s board: {engine_b.game.turn}\'s turn\n{engine_b.game.board}')
    #             match game.turn:
    #                 case 'white':
    #                     get_best_move(engine_w, 3, 5, False)
    #                 case 'black':
    #                     get_best_move(engine_b, 3, 5, False)
    #             print('Postmove board: \n',game.board)
    #             print(game)
    #     except Exception as e:
    #         print(f'Exception found: {e}')
    #     finally:
    #         end = time.perf_counter()
    #         print(f'Game took {(end-start)/60} min')

    # def test_depth_search_m3(self):
    #     print('======Play M3 position depth search======')
    #     game = Game()
    #     game.read_fen('7k/1R6/8/P1P5/4PPP1/8/8/6K1 w - - 3 37')
    #     engine_w = NaiveEngine(game, 'white', 5)
    #     engine_b = NaiveEngine(game, 'black', 5)

    #     start = time.perf_counter()
    #     try:
    #         while game.winner is None:
    #             print(f'Premove board: {game.turn}\'s turn\n',game.board)
    #             print(f'White\'s board: {engine_w.game.turn}\'s turn\n{engine_w.game.board}')
    #             print(f'Black\'s board: {engine_b.game.turn}\'s turn\n{engine_b.game.board}')
    #             match game.turn:
    #                 case 'white':
    #                     get_best_move(engine_w, 3, 5, False)
    #                 case 'black':
    #                     get_best_move(engine_b, 3, 5, False)
    #             print('Postmove board: \n',game.board)
    #     except Exception as e:
    #         print(f'Exception found: {e}')
    #     finally:
    #         end = time.perf_counter()
    #         print(f'Game took {(end-start)/60} min')