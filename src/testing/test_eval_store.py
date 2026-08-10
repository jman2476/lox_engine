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
        evals = EvalStore()

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
        evals = EvalStore()

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

        evals = EvalStore()

        for pos in to_store:
            evals.set_eval(*pos)

        for i in range(len(cases)):
            result = evals.get_eval(cases[i])
            print(f"Case: {cases[i]}")
            print(f'Expected: {expected[i]}')
            print(f'Actual: {result}')
            print('-------------------------')
            self.assertEqual(result, expected[i])

    def test_get_set_eval_mp(self):
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

        ext_eval_store = EvalStore()

        def proc_set_task(eval_store, fen, eval, process_id):
            print(f'Process {process_id}')
            eval_store.set_locked_eval(fen, eval)
            print(f'Proc-{process_id} stored {fen}: {eval}')

        def proc_get_task(eval_store, fen, process_id):
            print(f'Process {process_id}')
            result = eval_store.get_locked_eval(fen)
            print(f'Proc-{process_id} stored {fen}: {result}')
            self.assertEqual(result, expected[process_id])

        if __name__ == 'src.testing.test_eval_store':
            print('\n==Running MP test: Eval Store set==\n')
            EvalManager.register('EvalStore', EvalStore)
            # dict_lock = Lock()

            with EvalManager() as manager:
                eval_store = manager.EvalStore()
                set_processes = []
                for i in range(len(to_store)):
                    p = Process(
                        target=proc_set_task, 
                        args=(eval_store, *to_store[i], i))
                    set_processes.append(p)
                    p.start()

                for p in set_processes:
                    p.join()

                print('\n---Finished storing evals---')

                get_processes = []
                for i in range(len(cases)):
                    p = Process(
                        target=proc_get_task,
                        args = (eval_store, cases[i], i))
                    get_processes.append(p)
                    p.start()

                for p in get_processes:
                    p.join()

                print('\n---Finished gettting evals---')
                ext_eval_store.set_positions(eval_store.get_positions())

        print(ext_eval_store)

    def test_get_set_collision(self):
        to_store = [
            ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34', 12.39),
            ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 300 34', 12.39),
            ('k7/3Q4/K7/8/8/8/8/8 b - - 0 1', -4.43),
            ('k7/3Q4/K7/8/8/8/8/8 w - - 0 1', 4.43),
            ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0.00),
            ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0.00),
            ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 49 1', 0.00),
            ('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 52 21', 1.0212),
            ('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 52 21', 1.3212)
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

        evals = EvalStore()

        for pos in to_store:
            if not evals.get_eval(pos[0])[1]:
                evals.set_eval(*pos)
            else:
                print(f'Pos {pos} already stored')

        self.assertEqual(len(evals.positions), 6)

        for i in range(len(cases)):
            result = evals.get_eval(cases[i])
            print(f"Case: {cases[i]}")
            print(f'Expected: {expected[i]}')
            print(f'Actual: {result}')
            print('-------------------------')
            self.assertEqual(result, expected[i])

    def test_get_set_collision_mp(self):
        to_store = [
            ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34', 12.39),
            ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 300 34', 12.39),
            ('k7/3Q4/K7/8/8/8/8/8 b - - 0 1', -4.43),
            ('k7/3Q4/K7/8/8/8/8/8 w - - 0 1', 4.43),
            ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0.00),
            ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0.00),
            ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 49 1', 0.00),
            ('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 52 21', 1.0212),
            ('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 52 21', 1.3212)
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
        ext_eval_store = EvalStore()
        
        def proc_set_task(eval_store, fen, eval, process_id):
            print(f'Process {process_id}')
            eval_store.set_locked_eval(fen, eval)
            print(f'Proc-{process_id} stored {fen}: {eval}')

        def proc_get_task(eval_store, fen, process_id):
            print(f'Process {process_id}')
            result = eval_store.get_locked_eval(fen)
            print(f'Proc-{process_id} stored {fen}: {result}')
            self.assertEqual(result, expected[process_id])

        if __name__ == 'src.testing.test_eval_store':
            print('\n==Running MP test: Eval Store Collision==\n')
            EvalManager.register('EvalStore', EvalStore)
            # dict_lock = Lock()

            with EvalManager() as manager:
                eval_store = manager.EvalStore()
                set_processes = []
                for i in range(len(to_store)):
                    p = Process(
                        target=proc_set_task, 
                        args=(eval_store, *to_store[i], i))
                    set_processes.append(p)
                    p.start()

                for p in set_processes:
                    p.join()

                print('\n---Finished storing evals---')

                get_processes = []
                for i in range(len(cases)):
                    p = Process(
                        target=proc_get_task,
                        args = (eval_store, cases[i], i))
                    get_processes.append(p)
                    p.start()

                for p in get_processes:
                    p.join()

                print('\n---Finished gettting evals---')
                ext_eval_store.set_positions(eval_store.get_positions())

        print(ext_eval_store)