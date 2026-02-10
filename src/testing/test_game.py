import unittest
from src.game import Game
from src.board import Board

class TestGame(unittest.TestCase):
    def test_set_fen(self):
        game = Game()

        self.assertEqual(game.fen, '8/8/8/8/8/8/8/8 w - - 0 1')

        game.start_new_game()

        self.assertEqual(game.fen, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def test_read_fen(self):
        game = Game()
        ref_board = Board()

        game.read_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        ref_board.setup_new()

        self.assertEqual(
            game.board.__repr__(),
            ref_board.__repr__()
        )

        self.assertEqual(
            game.castling,
            'KQkq'
        )

        game.read_fen('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 2 21')
        
        self.assertEqual(
            game.turn,
            'black'
        )
        
        self.assertEqual(
            game.fullmove, 21
        )
        self.assertEqual(
            game.halfmove, 2
        )

    def test_repr(self):
        game = Game()

        game.start_new_game()

        self.assertEqual(
            game.__repr__(),
            game.fen
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