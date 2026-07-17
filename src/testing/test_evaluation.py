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
        board.setup_by_fen('KQ6/8/8/8/8/8/8/k5b1 w - - 0 1')
        sides = ['white', 'black']
        k_safety = []
        for s in sides:
            _, k_atk = space_control(board, s)
            k_safety.append(k_atk)

        print('King attacks: ')
        print(f'white: {k_safety[0].squares}')
        print(f'black: {k_safety[1].squares}')
        
        board.setup_by_fen('KQ6/8/8/8/8/2N5/6b1/k5b1 w - - 0 1')
        for s in sides:
            _, k_atk = space_control(board, s)
            k_safety.append(k_atk)
        
        print('King attacks: ')
        print(f'white: {k_safety[2].squares}')
        print(f'black: {k_safety[3].squares}')

        equality_asserts= [
            {'b1': 2, 'b2': 2},
            {'a7': 2},
            {'b1': 4, 'b2': 2, 'a2': 2},
            {'a7': 2,'a8': 2, 'b7': 2}
        ]
        
        for i, k_s in enumerate(k_safety):
            for key in k_s.squares:
                self.assertTrue(key in equality_asserts[i])
                print(f'expected: {key}: {equality_asserts[i][key]}')
                print(f'real: {key}: {k_s.squares[key]}')
                self.assertTrue(
                    k_s.squares[key] == equality_asserts[i][key]
                )

        # self.assertEqual(k_safety[0].squares,
        #                  {'b1': 2, 'b2': 2})
        # self.assertEqual(k_safety[1].squares,
        #                  {'a7': 2})
        # self.assertEqual(k_safety[2].squares,
        #                  {'b1': 4, 'b2': 2, 'a2': 2})
        # self.assertEqual(k_safety[3].squares,
        #                  {'a7': 2,'a8': 2, 'b7': 2})
        
