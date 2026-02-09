import unittest
from src.piece import King, Pawn
from src.board import Board

class TestKing(unittest.TestCase):
    def test_init(self):
        w_king = King('white', 'e1')
        b_king = King('black', 'e8')
        
        self.assertEqual(w_king.side, 'white')
        self.assertEqual(b_king.side, 'black')
        self.assertEqual(w_king.rank, 1)
        self.assertEqual(b_king.rank, 8)
        self.assertEqual(w_king.file, 'e')
        self.assertEqual(b_king.file, 'e')
        self.assertEqual(w_king.in_start_pos, True)
        self.assertEqual(b_king.in_check, False)
        self.assertEqual(w_king.icon, '\u2654')
        self.assertEqual(b_king.icon, '\u265A')
       
    def test_move_valid(self):
        w_king = King('white', 'e1')
        b_king = King('black', 'f5')
        b_king.in_start_pos = False
        board = Board()
        board.board['e'][1] = w_king
        board.board['f'][4] = b_king

        self.assertTrue(w_king.move_valid(2, 'e', board))
        self.assertTrue(b_king.move_valid(5, 'g', board))
        self.assertTrue(b_king.move_valid(6, 'g', board))

        with self.assertRaises(ValueError):
            b_king.move_valid(6, 'g', board)
            w_king.move_valid(4, 'g', board)

            
    def test_move(self):
        board = Board()
        board.setup_new()
        king = board.board['e'][0]
        pawn = board.board['e'][1]
        pawn.move(board, 'e4')
        king.move(board, 'e2')
        comparison_board = Board()
        comparison_board.setup_new()
        comparison_board.board['e'][0] = None
        comparison_board.board['e'][1] = King('white', 'e2')
        comparison_board.board['e'][3] = Pawn('white', 'e4')

        # print('Board\n', board)
        # print('Comp\n', comparison_board)

        self.assertFalse(king.in_start_pos)
        self.assertEqual((king.file, king.rank),('e', 2))
        self.assertEqual(board.__repr__(), comparison_board.__repr__())