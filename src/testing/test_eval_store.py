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