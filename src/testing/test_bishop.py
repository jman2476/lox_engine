import unittest
from src.piece import Pawn, Bishop
from src.board import Board
from src.functions.parse import parse_square

class TestBishop(unittest.TestCase):
    def test_init(self):
        bishop = Bishop('white', 'b5')
        self.assertIsInstance(bishop, Bishop)
        self.assertEqual(bishop.side, 'white')
        self.assertEqual(bishop.rank, 5)
        self.assertEqual(bishop.file, 'b')
        self.assertEqual(bishop.icon, '\u2657')

    def test_move_valid(self):
        bishop_w = Bishop('white', 'a4')
        bishop_b = Bishop('black', 'e5')
        pawn_w = Pawn('white', 'b3')
        pawn_b = Pawn('black', 'd7')
        board = Board()
        pieces = [bishop_w, bishop_b, pawn_b, pawn_w]
        
        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p

        # print(f'Bishop Movement\n{board}')
        self.assertTrue(bishop_w.move_valid(7, 'd', board))
        self.assertTrue(bishop_w.move_valid(6, 'c', board))
        self.assertTrue(bishop_b.move_valid(2, 'h', board))
        self.assertTrue(bishop_b.move_valid(1, 'a', board))
        self.assertTrue(bishop_b.move_valid(8, 'b', board))
        self.assertTrue(bishop_b.move_valid(8, 'h', board))
        
        with self.assertRaises(ValueError):
            bishop_b.move_valid(4, 'c', board)
        with self.assertRaises(ValueError):
            bishop_w.move_valid(3, 'b', board)
        with self.assertRaises(ValueError):
            bishop_w.move_valid(8, 'e', board)
        