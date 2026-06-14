import unittest
from src.game import Game
from src.functions.parse import (
    parse_square
)
from src.functions.direction import (
    get_direction,
    adjacent_squares
)

class TestAdjacentSquares(unittest.TestCase):
    def test_find_by_a1(self):
        game = Game()
        game.start_new_game()
        file, rank = parse_square("a1")
        adjacent = adjacent_squares(game.board, file, rank)
        print(f'Adjacent squares: {adjacent}\n')

        self.assertEqual(
            adjacent,
            [('b',1),('b',2),('a',2)]
        )
        