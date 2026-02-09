import unittest
from src.piece import Knight, Pawn
from src.board import Board
from src.functions.parse import parse_square

class TestKnight(unittest.TestCase):
    def test_init(self):
        knight = Knight('white', 'b1')
        self.assertIsInstance(knight, Knight)
        self.assertEqual(knight.side, 'white')
        self.assertEqual(knight.rank, 1)
        self.assertEqual(knight.file, 'b')
        self.assertEqual(knight.icon, '\u2658')
        
    def test_move_valid(self):
        knight = Knight('white', 'd4')
        pawn_w = Pawn('white', 'e2')
        pawn_b = Pawn('black', 'e6')
        board = Board()
        pieces = [knight, pawn_b, pawn_w]

        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p

        print(f'Knight Movement\n{board}')
        
        self.assertTrue(knight.move_valid(2, 'c', board))
        self.assertTrue(knight.move_valid(3, 'b', board))
        self.assertTrue(knight.move_valid(5, 'b', board))
        self.assertTrue(knight.move_valid(6, 'c', board))
        self.assertTrue(knight.move_valid(6, 'e', board))
        self.assertTrue(knight.move_valid(5, 'f', board))
        self.assertTrue(knight.move_valid(3, 'f', board))
        

        with self.assertRaises(ValueError):
            knight.move_valid(2, 'e', board)