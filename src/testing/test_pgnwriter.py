import unittest
from src.functions.game_writer import PGNWriter
from src.game import Game

class TestPGNWriter(unittest.TestCase):
    dir = './pgn-writer-testing'

    def test_create_header(self):
        game = Game()
        pgnw = PGNWriter(game, self.dir)
        pgnw.create_file()