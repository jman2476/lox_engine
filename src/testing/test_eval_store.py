import unittest
from multiprocessing import Process, Lock
from src.eval_store import EvalManager, EvalStore

class TestEvalStore(unittest.TestCase):
    def test_set_key(self):
        cases = ['6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34',
                'k7/3Q4/K7/8/8/8/8/8 b - - 0 1',
                 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                 '5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 52 21'
                 ]
        expected = ['6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8|w|F',
                'k7/3Q4/K7/8/8/8/8/8|b|F',
                 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR|w|F',
                 '5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2|b|T'
                 ]
        evals = EvalStore(Lock)

        for i in range(len(cases)):
            key = evals.set_key(cases[i])
            self.assertEqual(key, expected[i])

    def test_parse_key(self):
        cases = ['6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8|w|F',
                'k7/3Q4/K7/8/8/8/8/8|b|F',
                'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR|w|F',
                '5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2|b|T'
                ]
        expected = [('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8','w', False),
                    ('k7/3Q4/K7/8/8/8/8/8', 'b', False),
                    ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', 'w', False),
                    ('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2', 'b', True)
                    ]
        evals = EvalStore(Lock)

        for i in range(len(cases)):
            parsed_key = evals.parse_key(cases[i])
            self.assertEqual(parsed_key, expected[i])

    def test_get_set_eval(self):
        to_store = [
            ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34', 12.39),
            ('k7/3Q4/K7/8/8/8/8/8 b - - 0 1', -4.43),
            ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0.00),
            ('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 52 21', 1.0212)
            ]
        cases = [
            '6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34',
            'k7/3Q4/K7/8/8/8/8/8 b - - 0 1',
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
            '5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 52 21',
            '4rbk1/2q2ppB/p6p/P1n5/2Q5/1P5P/2Pr1PP1/R3R1K1 b - - 1 27'
            ]
        expected = [
            (12.39, True),
            (-4.43, True),
            (0.00, True),
            (1.0212, True),
            (None, False)
        ]

        evals = EvalStore(Lock)

        for pos in to_store:
            evals.set_eval(*pos)

        for i in range(len(cases)):
            result = evals.get_eval(cases[i])
            print(f"Case: {cases[i]}")
            print(f'Expected: {expected[i]}')
            print(f'Actual: {result}')
            print('-------------------------')
            self.assertEqual(result, expected[i])
