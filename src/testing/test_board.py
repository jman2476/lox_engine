import unittest
from src.board import Board
from src.piece import King, Queen, Rook

class TestBoard(unittest.TestCase):
    def test_setup_new(self):
        board = Board()
        board.setup_new()
        self.assertIsInstance(board.board['e'][0], King)
        self.assertIsNone(board.board['g'][4])
        self.assertIsInstance(board.board['h'][7], Rook)

    def test_set_back_rank(self):
        board = Board()
        self.assertEqual(board.set_back_rank('a'), Rook)
        self.assertEqual(board.set_back_rank('d'), Queen)
        self.assertEqual(board.set_back_rank('e'), King)
        
    def test_check_square_filled(self):
        board = Board()
        board.setup_new()
        f5 = board.check_square_filled('f', 5)
        e7 = board.check_square_filled('e', 7)
        self.assertFalse(f5[0])
        self.assertIsNone(f5[1])
        self.assertTrue(e7[0])
        self.assertEqual(e7[1], 'black')
