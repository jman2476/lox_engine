import unittest
from src.game import Game

class TestGameEnd(unittest.TestCase):
    def test_checkmate_cornerA(self):
        print('--Test checkmate corner A--')
        game = Game()
        fen = 'k7/3Q4/K7/8/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game)

        game.parse_move('Qb7')

        self.assertEqual(game.winner, '1-0')

    def test_checkmate_cornerB(self):
        print('--Test checkmate corner B--')
        game = Game()
        fen = 'k7/3Q4/K7/8/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game)

        game.parse_move('Qa7')

        self.assertEqual(game.winner, '1-0')

    def test_stalemate_corner(self):
        print('--Test stalemate corner --')
        game = Game()
        fen = 'k7/3Q4/K7/8/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)

        game.parse_move('Qc7')

        self.assertEqual(game.winner, '1/2-1/2')
    
    def test_backrank_mateA(self):
        print('--Test checkmate corner B--')
        game = Game()
        fen = 'k7/3R4/K7/8/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)

        game.parse_move('Rd8')

        self.assertEqual(game.winner, '1-0')

    def test_insufficient_material_knight(self):
        print("--Test insufficient: knight only--")
        game = Game()
        fen = 'k7/7N/8/K7/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)
        game.parse_move('Nf8')

        self.assertEqual(game.winner, '1/2-1/2')

    def test_insufficient_material_bishop(self):
        print("--Test insufficient: bishop only--")
        game = Game()
        fen = 'k7/7B/8/K7/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)
        game.parse_move('Bg8')

        self.assertEqual(game.winner, '1/2-1/2')

    def test_insufficient_material_kings(self):
        print("--Test insufficient: kings only--")
        game = Game()
        fen = 'k7/8/8/K7/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)
        game.parse_move('Ka6')

        self.assertEqual(game.winner, '1/2-1/2')
        

    def test_insufficient_material_w_timeout(self):
        print("--Test insufficient: white timeout--")
        game = Game()
        fen = 'k7/8/8/KQ6/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)

        self.assertEqual(
            game.board.sufficient_material(w_timeout=True), 
            False)
        

    def test_insufficient_material_b_timeout(self):
        print("--Test insufficient: black timeout--")
        game = Game()
        fen = 'krr5/7N/8/K7/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)
        game.parse_move('Nf8')

        self.assertEqual(
            game.board.sufficient_material(b_timeout=True), 
            False)
        
    def test_sufficient_material_b_timeout(self):
        print('--Test sufficient: black timeout--')
        game = Game()
        fen = 'krr5/7N/8/K6Q/8/8/8/8 w - - 0 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)
        game.parse_move('Nf8')

        self.assertEqual(
            game.board.sufficient_material(b_timeout=True), 
            True)