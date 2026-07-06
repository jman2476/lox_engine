from src.engines.fool import FoolEngine
from src.game import Game
import unittest

class TestFoolEngine(unittest.TestCase):
    def test_create_fool(self):
        print('---Test create fool engine instance---')
        game = Game()
        game.start_new_game()
        i_engine_w = FoolEngine(game, 'white')

        print(f'Engine: {i_engine_w}')
        print(i_engine_w.find_moves())

        game.parse_move('e4')
        print(f'Engine: {i_engine_w}')
        print(i_engine_w.find_moves())

    def test_play_move_fool(self):
        print('---Test fool engine: Play move random---')
        game = Game()
        game.start_new_game()
        i_engine_w = FoolEngine(game, 'white')

        print('Playing first move')
        i_engine_w.pick_and_play_move()
        print('Playing second move')
        i_engine_w.pick_and_play_move()
