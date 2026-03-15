import unittest
from src.functions.game_writer import read_pgn
import os

class TestReadPGN(unittest.TestCase):
    def test_read_pgn_erigaisi_abdusattorov(self):
        file_name = 'erigaisi-abdusattorov_Tata26.pgn'
        print("Erigaisi v Abdusattorov")
        moves, result = read_pgn(file_name, './test_pgn_files')

        # print(moves, result)

    def test_read_pgn_rozman_rosen(self):
        file_name = 'rozman-rosen_Blitz_May26.pgn'
        print("Rozman v Rosen")
        moves, result = read_pgn(file_name, './test_pgn_files')

        # print(moves, result)