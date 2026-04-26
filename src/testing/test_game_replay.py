import unittest
from src.functions.game_replay import game_replay

class TestGameReplay(unittest.TestCase):
    def test_replay_erigaisi_abdusattorov(self):
        file_name = 'erigaisi-abdusattorov_Tata26.pgn'
        print('Erigaisi v. Abdusattorov Tata \'26')
        # game_replay(file_name, './test_pgn_files')

    def test_replay_keymer_rameshbabu(self):
        file_name = 'keymer-rameshbabu_Tata26.pgn'
        print('Keymer v. Rameshbabu Tata \'26')
        # game_replay(file_name, './test_pgn_files')
        
    def test_replay_magnus_hikaru(self):
        file_name = 'magnus-hikaru_TT_May24.pgn'
        print('Magnus v. Hikaru Title Tues \'24')
        # game_replay(file_name, './test_pgn_files')
        
    def test_replay_rozman_rosen(self):
        file_name = 'rozman-rosen_Blitz_May26.pgn'
        print('Rozman v. Rosen Blitz May \'26')
        # game_replay(file_name, './test_pgn_files')
        
    def test_pawn_move_game(self):
        file_name = 'pawn_move_test.pgn'
        print('Pawn move example game')
        # game_replay(file_name, './test_pgn_files')