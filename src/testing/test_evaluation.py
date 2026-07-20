import unittest
from src.functions.evaluation import (
    get_evaluation,
    count_material, 
    space_control,
    calc_king_safety
)
from src.board import Board
from src.piece import *

class TestEvaluation(unittest.TestCase):
    def test_king_safety(self):
        print('-----Test King Safety-----')
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
        print(board)
        for s in sides:
            _, k_atk = space_control(board, s)
            k_safety.append(k_atk)
            print(f'side: {s}, {k_atk}')
        
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

    def test_calc_king_safety(self):
        print('----Calc King Safety----')
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

        computed_king_safety = []
        for s in sides:
            i = 0 if s == 'side' else 1
            k_s_val = calc_king_safety(board, s, k_safety[i])
            computed_king_safety.append(k_s_val)
        
        print('Computed King Safety')
        print(f'white: {computed_king_safety[0]}')
        print(f'black: {computed_king_safety[1]}')