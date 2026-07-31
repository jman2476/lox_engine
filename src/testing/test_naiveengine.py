from src.engines.naive import NaiveEngine
from src.game import Game
import unittest

class TestNaive(unittest.TestCase):
    def test_fen_to_key(self):
        game = Game()
        game.start_new_game()
        engine = NaiveEngine(game, 'white')

        start_pos_key = engine.fen_to_key()

        self.assertEqual(start_pos_key, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -')

        game.parse_move('e4')

        next_pos_key = engine.fen_to_key()

        self.assertEqual(next_pos_key, 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3')
        