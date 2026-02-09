import unittest
from src.piece import King, Pawn, Rook
from src.board import Board
from src.functions.parse import parse_square

class TestRook(unittest.TestCase):
    def test_init(self):
        rook = Rook('white', 'a1')
        self.assertIsInstance(rook, Rook)
        self.assertEqual(rook.side, 'white')
        self.assertEqual(rook.rank, 1)
        self.assertEqual(rook.file, 'a')
        self.assertEqual(rook.icon, '\u2656')

    def test_move_valid(self):
        rook = Rook('white', 'd4')
        w_pawn = Pawn('white', 'g4')
        b_pawn = Pawn('black', 'd7')
        king = King('black', 'd8')
        board = Board()
        pieces = [rook, w_pawn, b_pawn, king]

        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p

        print(f'Board\n{board}')
        self.assertTrue(rook.move_valid(2, 'd', board))
        self.assertTrue(rook.move_valid(7, 'd', board))
        self.assertTrue(rook.move_valid(4, 'a', board))
        self.assertTrue(rook.move_valid(4, 'e', board))

        with self.assertRaises(ValueError):
            rook.move_valid(8, 'd', board)
            rook.move_valid(1, 'a', board)
            rook.move_valid(4, 'g', board)
