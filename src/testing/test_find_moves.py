import unittest
from src.game import Game
from src.functions.find_moves import (
        find_available_moves,
        find_pawn_moves
        )
from src.piece import (
        Pawn, King,
        Queen, Bishop
        )

class TestFindMoves(unittest.TestCase):
    def test_find_available(self):
        game = Game()
        game.start_new_game()
        w_pieces = game.board.white()
        moves = []
        for piece in w_pieces:
            moves.append([piece, find_available_moves(game.board, piece)])

        print("Available moves:\n", moves)

    def test_find_pawn_moves(self):
        game = Game()
        game.start_new_game()
        w_pawns = [pawn for pawn in game.board.white() if isinstance(pawn, Pawn)]

        for pawn in w_pawns:
            moves = find_pawn_moves(game.board, pawn)
            print(f'moves for {pawn}: {moves}')
        
        game.parse_move('e4')
        game.parse_move('d5')
        w_pawns = [pawn for pawn in game.board.white() if isinstance(pawn, Pawn)]
        
        for pawn in w_pawns:
            moves = find_pawn_moves(game.board, pawn)
            print(f'moves for {pawn}: {moves}')
        


