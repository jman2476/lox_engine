from src.engines.fast_engine import FastEngine
from src.game import Game
import unittest

class TestFastEngine(unittest.TestCase):
    def test_init(self):
        game = Game()
        game.start_new_game()
        engine = FastEngine(game, 'white', (2,3))

        self.assertEqual(engine.search, (2,3))
        self.assertEqual(engine.name, 'fast')