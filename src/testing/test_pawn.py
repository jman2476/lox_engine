import unittest
from src.piece import Pawn
from src.board import Board

class TestPawn(unittest.TestCase):
    def test_init(self):
        w_pawn = Pawn('white', 'a2')
        b_pawn = Pawn('black', 'g7')
        
        self.assertEqual(w_pawn.side, 'white')
        self.assertEqual(b_pawn.side, 'black')
        self.assertEqual(w_pawn.rank, 2)
        self.assertEqual(b_pawn.rank, 7)
        self.assertEqual(w_pawn.file, 'a')
        self.assertEqual(b_pawn.file, 'g')
        self.assertEqual(w_pawn.in_start_pos, True)
        self.assertEqual(b_pawn.in_start_pos, True)
        self.assertEqual(w_pawn.icon, '\u2659')
        self.assertEqual(b_pawn.icon, '\u265F')
       
    def test_move_valid(self):
        w_pawnA = Pawn('white', 'a2')
        w_pawnB = Pawn('white', 'f5')
        b_pawnA = Pawn('black', 'g7')
        b_pawnB = Pawn('black', 'g6')
        b_pawnB.in_start_pos = False
        board = Board()
        board.board['a'][1] = w_pawnA
        board.board['f'][4] = w_pawnB
        board.board['g'][6] = b_pawnA
        board.board['g'][5] = b_pawnB

        self.assertTrue(w_pawnA.move_valid(4, 'a', board))
        self.assertTrue(b_pawnB.move_valid(5, 'g', board))
        self.assertTrue(w_pawnB.move_valid(6, 'g', board))

        with self.assertRaises(ValueError):
            b_pawnA.move_valid(6, 'g', board)
            b_pawnB.move_valid(4, 'g', board)
            w_pawnA.move_valid(2, 'b', board)
            
    def test_move(self):
        board = Board()
        board.setup_new()
        pawn = board.board['d'][1]
        pawn.move(board, 'd4')
        comparison_board = Board()
        comparison_board.setup_new()
        comparison_board.board['d'][1] = None
        comparison_board.board['d'][3] = Pawn('white', 'd4')

        self.assertFalse(pawn.in_start_pos)
        self.assertEqual((pawn.file, pawn.rank),('d', 4))
        self.assertEqual(board.__repr__(), comparison_board.__repr__())

if __name__ == '__main__':
    unittest.main()
