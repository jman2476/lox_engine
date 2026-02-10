import unittest
from src.game import Game

class TestGame(unittest.TestCase):
    def test_set_fen(self):
        game = Game()

        self.assertEqual(game.fen, '8/8/8/8/8/8/8/8 w - - 0 1')

        game.start_new_game()

        self.assertEqual(game.fen, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def test_repr(self):
        game = Game()

        game.start_new_game()

        self.assertEqual(
            print(game),
            print(game.fen)
        )

    def test_get_castle_state(self):
        game = Game()
        game.start_new_game()
        b = game.board

        self.assertEqual(
            game.get_castle_state(),
            'KQkq'
        )

        rpawn = b.board['a'][6]
        rook = b.board['a'][7]
        rpawn.move(b, 'a6')
        rook.move(b, 'a7')

        self.assertEqual(
            game.get_castle_state(),
            'KQk'
        )

        Kpawn = b.board['e'][1]
        king = b.board['e'][0]
        Kpawn.move(b, 'e4')
        king.move(b, 'e2')

        self.assertEqual(
            game.get_castle_state(),
            'k'
        )