from src.engines.fast_engine import FastEngine
from src.game import Game
import unittest

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