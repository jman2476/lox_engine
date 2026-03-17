import unittest
from src.game import Game
from src.functions.find_moves import (
        find_available_moves,
        find_pawn_moves
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
        pass


