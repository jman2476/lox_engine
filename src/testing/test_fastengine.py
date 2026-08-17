from src.engines.fast_engine import FastEngine
from src.game import Game
import unittest, time

class TestFastEngine(unittest.TestCase):
    def test_init(self):
        game = Game(dir='./test_games')
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))

        self.assertEqual(engine.search, (2,3))
        self.assertEqual(engine.name, 'fast')

    def test_find_moves(self):
        print('===Test Find Moves===')
        game = Game(dir='./test_games')
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))

        starting_moves = engine.find_moves()
        print(f'Type of move list: {type(starting_moves[0])}')

        self.assertEqual(len(starting_moves), 20)

    def test_eval_moves(self):
        print("---Test Eval Moves---")
        game = Game(dir='./test_games')
        game.read_fen('k7/3Q4/K7/8/8/8/8/8 w - - 0 1')
        engine = FastEngine(game, 'white', (2,3))
        move_list = ['Qa7', 'Qb7', 'Qc7', 'Ka5']

        move_evals = engine.eval_moves(move_list)
        print(f'Evaluated moves: {move_evals}')

        for mv in move_evals:
            match mv[0]:
                case 'Qa7':
                    self.assertEqual(mv[1], 1000.0)
                case 'Qb7':
                    self.assertEqual(mv[1], 1000.0)
                case 'Qc7':
                    self.assertEqual(mv[1], 0.0)
                case 'Ka5':
                    self.assertTrue(mv[1] > 0)

        engine.game.read_fen('K7/3q4/k7/8/8/8/8/8 b - - 0 1')
        move_list = ['Qa7', 'Qb7', 'Qc7', 'Ka5']
        move_evals = engine.eval_moves(move_list)
        print(f'Evaluated moves: {move_evals}')
        for mv in move_evals:
            match mv[0]:
                case 'Qa7':
                    self.assertEqual(mv[1], -1000.0)
                case 'Qb7':
                    self.assertEqual(mv[1], -1000.0)
                case 'Qc7':
                    self.assertEqual(mv[1], 0.0)
                case 'Ka5':
                    self.assertTrue(mv[1] < 0)

    def test_rank_moves(self):
        game = Game(dir='./test_games')
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))
        move_evals = [
            ('e4', 10.0),
            ('d4', 12.0),
            ('Nc3', 6.2),
            ('Na3', -3),
            ('b3', -100),
            ('Nf3', 200),
            ('Nh3', -1.0),
            ('h4', 6.3)
        ]
        expected_order_w = [
            ('Nf3', 200),
            ('d4', 12.0),
            ('e4', 10.0),
            ('h4', 6.3),
            ('Nc3', 6.2),
            ('Nh3', -1.0),
            ('Na3', -3),
            ('b3', -100),
        ]
        expected_order_b = expected_order_w.copy()
        expected_order_b.reverse()

        ranked_white = engine.rank_moves(move_evals)
        self.assertEqual(ranked_white, expected_order_w)

        game.parse_move('e4')

        ranked_black = engine.rank_moves(move_evals)
        self.assertEqual(ranked_black, expected_order_b)

    def test_rank_moves_long(self):
        game = Game(dir='./test_games')
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))
        move_evals = [
            ('e4', 10.0),
            ('d4', 12.0),
            ('Nc3', 6.2),
            ('Na3', -3),
            ('b3', -100),
            ('Nf3', 200),
            ('Nh3', -1.0),
            ('h4', 6.3),
            ('a3', -200),
            ('a4', -199),
            ('b4', -201),
            ('c3', -201)
        ]
        expected_order_w = [
            ('Nf3', 200),
            ('d4', 12.0),
            ('e4', 10.0),
            ('h4', 6.3),
            ('Nc3', 6.2),
            ('Nh3', -1.0),
            ('Na3', -3),
            ('b3', -100),
            ('a4', -199),
            ('a3', -200),
        ]
        expected_order_b = [
            ('e4', 10.0),
            ('h4', 6.3),
            ('Nc3', 6.2),
            ('Nh3', -1.0),
            ('Na3', -3),
            ('b3', -100),
            ('a4', -199),
            ('a3', -200),
            ('c3', -201),
            ('b4', -201),
        ]
        expected_order_b.reverse()

        ranked_white = engine.rank_moves(move_evals)
        self.assertEqual(ranked_white, expected_order_w)

        game.parse_move('e4')

        ranked_black = engine.rank_moves(move_evals)
        self.assertEqual(ranked_black, expected_order_b)

    def test_rank_moves_empty(self):
        game = Game()
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))
        self.assertEqual(engine.rank_moves([]), [])

    def test_eval_speed(self):
        game = Game()
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,2))

        start_1 = time.perf_counter()
        moves_1 = engine.find_ranked_moves()
        end_1 = time.perf_counter()

        start_2 = time.perf_counter()
        moves_2 = engine.find_ranked_moves()
        end_2 = time.perf_counter()

        dif_1 = end_1 - start_1
        dif_2 = end_2 - start_2

        self.assertEqual(moves_1, moves_2)
        print(f'Run 1: {dif_1}s')
        print(f'Run 2: {dif_2}s')
        print(f'Diff 2-1: {dif_2 - dif_1}s')
        self.assertTrue(dif_2 < dif_1)