import unittest
from src.game import Game

class TestGame(unittest.TestCase):
    def test_set_fen(self):
        game = Game()

        self.assertEqual(game.fen, '8/8/8/8/8/8/8/8 w - - 0 1')

        game.start_new_game()

        self.assertEqual(game.fen, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
