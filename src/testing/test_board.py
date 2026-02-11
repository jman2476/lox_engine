import unittest
from src.board import Board
from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook)
from src.functions.parse import parse_square

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
        print(f'All checks board: {board}')

        self.assertEqual(checks, [])

        board.setup_by_fen('4rbk1/2q2ppB/p6p/P1n5/2Q5/1P5P/2Pr1PP1/R3R1K1 b - - 1 27')
        checks = board.find_checks('g8', 'black')

        bishop = board.board['h'][6]
        self.assertEqual(checks, [bishop])

    def test_next_piece_hor(self):
        board = Board()
        king = King('white', 'd4')
        queen = Queen('black', 'g4')
        queen_w = Queen('white', 'h4')
        rook = Rook('white', 'a4')
        pawn = Pawn('white', 'b4')
        pieces = [king, queen, queen_w, rook]

        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p

        sight_arr = board.next_piece('horizontal')('d',4)
        # print(board)
        self.assertEqual(
            sight_arr, [rook, queen]
        )

        board.board['b'][3] = pawn
        # print(board)
        sight_two = board.next_piece('horizontal')('d',4)
        self.assertEqual(
            sight_two, [None, queen]
        )

    def test_next_piece_vert(self):
        board = Board()
        king = King('white', 'd4')
        queen = Queen('black', 'd7')
        queen_w = Queen('white', 'd8')
        rook = Rook('white', 'd1')
        pawn = Pawn('white', 'd2')
        pieces = [king, queen, queen_w, rook]

        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p

        sight_arr = board.next_piece('vertical')('d',4)
        # print(board)
        self.assertEqual(
            sight_arr, [rook, queen]
        )

        board.board['d'][1] = pawn
        # print(board)
        sight_two = board.next_piece('vertical')('d',4)
        self.assertEqual(
            sight_two, [None, queen]
        )

    def test_next_piece_b_diag(self):
        board = Board()
        king = King('white', 'd4')
        queen = Queen('black', 'a7')
        queen_w = Queen('white', 'b6')
        bishop = Bishop('white', 'g1')
        pawn = Pawn('white', 'f2')
        pawn_2 = Pawn('white', 'e3')
        pieces = [king, queen, queen_w, bishop]

        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p

        sight_arr = board.next_piece('back_diagonal')('d',4)
        # print(board)
        self.assertEqual(
            sight_arr, [queen_w, bishop]
        )

        board.board['f'][1] = pawn
        # print(board)
        sight_two = board.next_piece('back_diagonal')('d',4)
        self.assertEqual(
            sight_two, [queen_w, None]
        )
        board.board['e'][2] = pawn_2
        # print(board)
        sight_two = board.next_piece('back_diagonal')('d',4)
        self.assertEqual(
            sight_two, [queen_w, pawn_2]
        )

    def test_next_piece_f_diag(self):
        board = Board()
        king = King('white', 'd4')
        queen = Queen('black', 'h8')
        queen_w = Queen('white', 'g7')
        bishop = Bishop('white', 'a1')
        pawn = Pawn('white', 'b2')
        pawn_2 = Pawn('black', 'e5')
        pieces = [king, queen, queen_w, bishop]

        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p

        sight_arr = board.next_piece('forward_diagonal')('d',4)
        # print(board)
        self.assertEqual(
            sight_arr, [bishop, queen_w]
        )

        board.board['b'][1] = pawn
        # print(board)
        sight_two = board.next_piece('forward_diagonal')('d',4)
        self.assertEqual(
            sight_two, [None, queen_w]
        )
        board.board['e'][4] = pawn_2
        # print(board)
        sight_two = board.next_piece('forward_diagonal')('d',4)
        self.assertEqual(
            sight_two, [None, pawn_2]
        )

    def test_next_piece_knight(self):
        board = Board()
        king = King('white', 'd4')
        queen = Queen('black', 'f5')
        knight = Knight('black', 'e6')
        knight2 = Knight('black', 'b3')
        knight3 = Knight('white', 'f3')
        knight4 = Knight('black', 'e2')
        knight5 = Knight('black', 'c2')
        pawn = Pawn('white', 'b5')
        pawn2 = Pawn('white', 'c6')
        pieces = [king, queen, knight, knight2, knight3]
        pieces2 = [knight4, knight5, pawn, pawn2]
        
        for p in pieces:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p
        print(board)
        horses = board.next_piece('knight')('d', 4)

        for p in pieces2:
            f, r = parse_square(p.square)
            board.board[f][r-1] = p
        print(board)
        horsies = board.next_piece('knight')('d', 4)
        
        self.assertEqual(
            horses, [knight, knight3, knight2]
        )
        self.assertEqual(
            horsies, [knight, knight3, knight4, knight5, knight2]
        )