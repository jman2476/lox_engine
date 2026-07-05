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
        
    def test_fifty_move_from_fen(self):
        print('--Test 50 move: from fen--')
        game = Game()
        fen = 'kq6/6QK/8/8/8/8/8/8 w - - 49 1'
        game.read_fen(fen)
        game.set_fen()
        # print(game.board)

        game.parse_move('Qf8')

        self.assertEqual(
            game.winner, '1/2-1/2'
        )

    def test_fifty_move_from_start(self):
        print('--Test 50 move: from start--')
        game = Game()
        game.start_new_game()
        move_list = ['Qh5', 'Qh4', 'Qd1', 'Qd8']

        game.parse_move('e4')
        game.parse_move('e5')

        while game.winner is None:
            for move in move_list:
                game.parse_move(move)
            game.board_states = {}

        self.assertEqual(
            game.winner, '1/2-1/2'
        )

    def test_fifty_move_from_start(self):
        print('--Test 50 move: from start--')
        game = Game()
        game.start_new_game()
        move_list = ['Qh5', 'Qh4', 'Qd1', 'Qd8']

        game.parse_move('e4')
        game.parse_move('e5')

        while game.halfmove < 48:
            for move in move_list:
                game.parse_move(move)
            game.board_states = {}
        
        game.parse_move('d4')

        self.assertEqual(
            game.winner, None
        )

        self.assertEqual(
            game.halfmove, 0
        )

    def test_threefold_repetition(self):
        print('--Test threefold repetition--')
        game = Game()
        game.start_new_game()
        move_list = ['Qh5', 'Qh4', 'Qd1', 'Qd8']
        move = 0

        game.parse_move('e4')
        game.parse_move('e5')

        while game.winner is None:
            game.parse_move(move_list[move%4])
            move += 1
            print(move_list[move%4], game.winner)
            print(game.board_states)
        


        self.assertEqual(
            game.winner, '1/2-1/2'
        )