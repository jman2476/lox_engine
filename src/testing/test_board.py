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

    def test_get_white_pieces(self):
        board = Board()
        board.setup_new()
        white_pieces = board.get_white_pieces()
        self.assertEqual(
            len(white_pieces), 16
        )
        
    def test_get_black_pieces(self):
        board = Board()
        board.setup_new()
        black_pieces = board.get_black_pieces()
        self.assertEqual(
            len(black_pieces), 16
        )

    def test_check_square_filled(self):
        board = Board()
        board.setup_new()
        f5 = board.check_square_filled('f', 5)
        e7 = board.check_square_filled('e', 7)
        self.assertFalse(f5[0])
        self.assertIsNone(f5[1])
        self.assertTrue(e7[0])
        self.assertEqual(e7[1], 'black')

    def test_setup_by_fen(self):
        board = Board()
        empty_FEN = '8/8/8/8/8/8/8/8 w - - 0 1'
        fen_arr, ranks = board.setup_by_fen(empty_FEN)

        self.assertEqual(
            len(fen_arr),
            6
        )
        self.assertEqual(
            len(ranks),
            8
        )
        self.assertEqual(
            ranks,
            ['8','8','8','8','8','8','8','8']
        )

        board.setup_by_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        comparison_board = Board()
        comparison_board.setup_new()
        # print('Fresh board by FEN:\n', board)
        # print('Fresh board by constructor:\n', comparison_board)
        self.assertEqual(
            board.__repr__(),
            comparison_board.__repr__()
        )

        board.setup_by_fen('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 2 21')
        # print('Fresh board by FEN 2:\n', board)
        white_rook = board.board['f'][0]
        black_rook = board.board['f'][7]
        white_pawn = board.board['a'][1]
        black_pawn = board.board['d'][5]

        self.assertEqual(
            white_rook.in_start_pos, False
        )
        self.assertEqual(
            black_rook.in_start_pos, False
        )
        self.assertEqual(
            white_pawn.in_start_pos, True
        )
        self.assertEqual(
            black_pawn.in_start_pos, False
        )

    def test_find_checks(self):
        board = Board()
        board.setup_new()
        checks = board.find_checks('e1', 'white')

        self.assertEqual(checks, [])