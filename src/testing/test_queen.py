import unittest
from src.piece import Queen, Pawn
from src.board import Board
from src.functions.parse import parse_square

class TestQueen(unittest.TestCase):
    def test_init(self):
        queen = Queen('white', 'd1')
        self.assertIsInstance(queen, Queen)
        self.assertEqual(queen.side, 'white')
        self.assertEqual(queen.rank, 1)
        self.assertEqual(queen.file, 'd')
        self.assertEqual(queen.icon, '\u2655')
        
    def test_move_valid(self):
        queen = Queen('white', 'd4')
        pawn_w = Pawn('white', 'd2')
        pawn_b = Pawn('black', 'd7')
        board = Board()
        pieces = [queen, pawn_b, pawn_w]

        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p

        print(f'Board\n{board}')
        
        self.assertTrue(queen.move_valid(7, 'd', board))
        self.assertTrue(queen.move_valid(4, 'a', board))
        self.assertTrue(queen.move_valid(8, 'h', board))
        
        with self.assertRaises(ValueError):
            queen.move_valid(2, 'd', board)
            queen.move_valid(8, 'd', board)
            queen.move_valid(8, 'h', board)