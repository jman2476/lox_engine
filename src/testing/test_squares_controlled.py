import unittest
from src.game import Game
from src.functions.squares_controlled import (
    find_squares_controlled,
    pawn_squares_controlled,
    king_squares_controlled,
    queen_squares_controlled,
    bishop_squares_controlled,
    knight_squares_controlled,
    rook_squares_controlled,
    ControlledSquares
)
from src.piece import (
    Pawn, King,
    Queen, Rook,
    Bishop, Knight
)
from src.functions.evaluation import space_control
import logging
logger = logging.getLogger(__name__)

class TestControlledSquares(unittest.TestCase):
    

    def test_find_squares_controlled(self):
        self.assertEqual(0,1)


    def test_find_pawn_control(self):
        print('-----Test: pawn squares controlled-----')
        game = Game()
        game.start_new_game()
        game.parse_move('e4')
        attacked = ControlledSquares()

        for p in game.board.white():
            if isinstance(p,Pawn):
                attacked += find_squares_controlled(game.board, p)  
                # logger.debug(f'current: {attacked}')

        print('all attacked squares', attacked.squares)
        self.assertEqual(
            {'b3': 2, 'a3': 1, 'c3': 2, 'd3': 1, 'e3': 2,
             'd5': 1, 'f5': 1, 'g3': 2, 'f3': 1, 'h3': 1}, 
            attacked.squares)

        self.assertEqual(
            {'d5': 1, 'f5': 1, 'a6': 1, 'b5': 1, 'h5': 1},
            space_control(game.board, 'white')[0].squares
        )
        

    def test_find_king_control(self):
        print('-----Test: king squares controlled-----')

        self.assertEqual(0,1)


    def test_find_queen_control(self):
        print('-----Test: queen squares controlled-----')
        game = Game()
        game.start_new_game()
        game.parse_move('e4')
        attacked = ControlledSquares()

        for p in game.board.white():
            if isinstance(p, Queen):
                attacked += find_squares_controlled(game.board, p)

        print('Queen squares attacked: ')
        print(attacked)
        self.assertEqual(0,1)


    def test_find_bishop_control(self):
        print('-----Test: bishop squares controlled-----')

        self.assertEqual(0,1)


    def test_find_knight_control(self):
        print('-----Test: knight squares controlled-----')
        game = Game()
        game.start_new_game()
        attacked = ControlledSquares()

        for p in game.board.white():
            if isinstance(p, Knight):
                attacked += find_squares_controlled(game.board, p)
        
        print('Knight squares attacked: ')
        print(attacked)
        expected = {
            'a3': 1, 'c3': 1,
            'f3': 1, 'h3': 1,
            'e2': 1, 'd2': 1
        }

        for sq in attacked.squares:
            self.assertTrue(sq in expected)
            self.assertTrue(
                attacked.squares[sq] == expected[sq]
            )
        # self.assertEqual(0,1)
        

    def test_find_rook_control(self):
        print('-----Test: rook squares controlled-----')

        self.assertEqual(0,1)