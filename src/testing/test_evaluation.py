import unittest
from src.functions.evaluation import (
    get_evaluation,
    count_material, 
    space_control
)
from src.board import Board
from src.piece import *

class TestEvaluation(unittest.TestCase):
    def test_king_safety(self):
        board = Board()
        board.setup_by_fen('KQ6/8/8/8/8/8/8/k7 w - - 0 1')
        sides = ['white', 'black']
        k_safety = []
        for s in sides:
            _, k_atk = space_control(board, s)
            k_safety.append(k_atk)

        print('King attacks: ')
        print(f'white: {k_safety[0].squares}')
        print(f'black: {k_safety[1].squares}')