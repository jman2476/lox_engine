import unittest
from src.functions.game_replay import game_replay

class TestGameReplay(unittest.TestCase):
    def test_replay_erigaisi_abdusattorov(self):
        file_name = 'erigaisi-abdusattorov_Tata26.pgn'
        game_replay(file_name, './test_pgn_files')
