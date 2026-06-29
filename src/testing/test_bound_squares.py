import unittest
from src.board import Board
from src.piece import (
    Pawn, King,
    Queen, Bishop,
    Knight, Rook
)
from src.functions.parse import parse_square

class TestBoundSquares(unittest.TestCase):
    def test_horizontal(self):
        board = Board()
        w_rook = Rook('white', 'd4')
        queen = Queen('white', 'f4')
        b_rook = Rook('black', 'b4')
        w_rook_b = Rook('white', 'b2')
        w_pawn_g = Pawn('white', 'g2')
        w_pawn_a = Pawn('white', 'a2')
        pieces = [w_rook, queen, b_rook, w_rook_b, w_pawn_g, w_pawn_a]
        
        for p in pieces:
            f, r = parse_square(p.square())
            board.board[f][r-1] = p
            
        print(board)
        
        bounds_fourth = board.bound_squares('horizontal')('d',4, 'white')
        self.assertEqual(bounds_fourth, ['b4', 'e4'])

        bounds_second = board.bound_squares('horizontal')('b', 2, 'white')
        self.assertEqual(bounds_second, ['b2', 'f2'])

    def test_vertical(self):
        ...

    def test_forward_diagonal(self):
        ...

    def test_back_diagonal(self):
        ...

    def test_knight(self):
        ...
