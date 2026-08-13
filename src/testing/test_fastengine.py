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
        ...