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
        print('--Test horizontal--')
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
        print('--Test vertical--')
        board = Board()
        w_rook = Rook('white', 'd4')
        w_queen = Queen('white', 'g6')
        w_pawn = Pawn('white', 'd2')
        b_pawn = Pawn('black', 'd6')
        w_bishop = Bishop('white', 'g1')
        pieces = [w_rook, w_queen, w_pawn, b_pawn, w_bishop]
        
        for p in pieces:
            f, r = parse_square(p.square())
            board.board[f][r-1] = p
            
        print(board)
        
        bounds_d = board.bound_squares('vertical')('d', 4, 'white')
        self.assertEqual(bounds_d, ['d3', 'd6'])
        
        bounds_g = board.bound_squares('vertical')('g', 6, 'white')
        self.assertEqual(bounds_g, ['g2', 'g8'])

    def test_forward_diagonal(self):
        ...

    def test_back_diagonal(self):
        print('--Test back diagonal--')
        board = Board()
        w_wbishop = Bishop('white', 'e4')
        w_bbishop = Bishop('white', 'a1')
        b_pawn = Pawn('black', 'b7')
        w_pawn = Pawn('white', 'g2')
        b_bishop = Bishop('black', 'd6')
        pieces = [w_wbishop, b_bishop, w_bbishop, b_pawn, w_pawn]

        for p in pieces:
            f, r = parse_square(p.square())
            board.board[f][r-1] = p
            
        print(board)
        
        bounds_wb = board.bound_squares('back_diagonal')('a', 1, 'white')
        self.assertEqual(bounds_wb, ['a1','a1']) 
        
        bounds_ww = board.bound_squares('back_diagonal')('e', 4, 'white')
        self.assertEqual(bounds_ww, ['b7', 'f3'])

        bounds_b = board.bound_squares('back_diagonal')('d', 6, 'black')
        self.assertEqual(bounds_b, ['b8', 'h2'])

    def test_knight(self):
        ...
