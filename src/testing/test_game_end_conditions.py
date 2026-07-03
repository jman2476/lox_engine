import unittest
from src.game import Game

class TestGameEnd(unittest.TestCase):
    def test_checkmate_cornerA(self):
        print('--Test checkmate corner A--')
        game = Game()
        fen = 'k7/3Q4/K7/8/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        print(game)

        game.parse_move('Qb7')

        self.assertEqual(game.winner, '1-0')

    def test_checkmate_cornerB(self):
        print('--Test checkmate corner B--')
        game = Game()
        fen = 'k7/3Q4/K7/8/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        print(game)

        game.parse_move('Qa7')

        self.assertEqual(game.winner, '1-0')

    def test_stalemate_corner(self):
        print('--Test stalemate corner --')
        game = Game()
        fen = 'k7/3Q4/K7/8/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        print(game)

        game.parse_move('Qc7')

        self.assertEqual(game.winner, '1/2-1/2')
    
    def test_backrank_mateA(self):
        print('--Test checkmate corner B--')
        game = Game()
        fen = 'k7/3R4/K7/8/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        print(game)

        game.parse_move('Rd8')

        self.assertEqual(game.winner, '1-0')