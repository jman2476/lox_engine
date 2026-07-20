import unittest
from src.pgn_writer import PGNWriter
from src.game import Game

class TestPGNWriter(unittest.TestCase):
    dir = './pgn-writer-testing'

    def test_create_header(self):
        game = Game()
        pgnw = PGNWriter(game, self.dir)
        pgnw.create_file()

    def test_set_moves(self):
        game = Game()
        pgnw = PGNWriter(game, self.dir)
        game.start_new_game()
        pgnw.create_file()
        move_list = ['e3', 'f5', 'f4', 'g5', 'Qh5']

        for mv in move_list:
            pgnw.add_move(game.turn, mv)
            game.parse_move(mv)

        pgnw.final_result()