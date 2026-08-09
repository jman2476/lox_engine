import unittest
from src.grug_eval_store import GrugEvalStore, GrugManager
import os, shutil
import multiprocessing as mp


class TestGrugEval(unittest.TestCase):
    def test_grug_mkdir(self):
        grug_eval_a = GrugEvalStore()
        self.assertEqual(os.path.exists('./grug_eval'), True)
        grug_a_ls = os.listdir('./grug_eval')
        self.assertEqual(len(grug_a_ls), 0)

        grug_eval_b = GrugEvalStore('./grug_eval_2')
        self.assertEqual(os.path.exists('./grug_eval_2'), True)
        grug_b_ls = os.listdir('./grug_eval_2')
        self.assertEqual(len(grug_b_ls), 0)

        dummy_file_path = os.path.join(grug_eval_a.path, 'test.txt')
        with open(dummy_file_path, 'w', encoding='UTF-8') as file:
            file.write('Potato test')
        grug_a_ls = os.listdir('./grug_eval')
        self.assertEqual(len(grug_a_ls), 1)

        grug_eval_a_2 = GrugEvalStore()
        grug_a_ls = os.listdir('./grug_eval')
        self.assertEqual(len(grug_a_ls), 0)

        shutil.rmtree(grug_eval_a_2.path)
        shutil.rmtree(grug_eval_b.path)

    def test_create_file_name(self):
        fen_a = 'k7/3Q4/K7/8/8/8/8/8 w - - 0 1'
        eval_a = 69.4201
        fen_b = '6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34'
        eval_b = -420.69

        grug_eval = GrugEvalStore()
        cases = [(fen_a, eval_a),
                 (fen_b, eval_b)]
        expected = ['"k7=3Q4=K7=8=8=8=8=8_w_69.42".txt',
                    '"6R1=8=2B5=4Q3=P1k2P1P=8=3K4=8_w_-420.69".txt']

        for i in range(2):
            file_name = grug_eval.create_file_name(*cases[i])
            self.assertEqual(file_name, expected[i])


    def test_parse_file_name(self):
        cases = ['"k7=3Q4=K7=8=8=8=8=8_w_69.42".txt',
                '"6R1=8=2B5=4Q3=P1k2P1P=8=3K4=8_w_-420.69".txt']
        expected = [('k7/3Q4/K7/8/8/8/8/8','w',69.42),
                    ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8','w',-420.69)]
        grug_eval = GrugEvalStore()

        for i in range(2):
            parsed_file = grug_eval.parse_file_name(cases[i])
            self.assertEqual(parsed_file, expected[i])


    def test_store_eval(self):
        fen_a = 'k7/3Q4/K7/8/8/8/8/8 w - - 0 1'
        eval_a = 69.4201
        fen_b = '6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34'
        eval_b = -420.69

        grug_eval = GrugEvalStore()
        cases = [(fen_a, eval_a),
                    (fen_b, eval_b)]

        for c in cases:
            grug_eval.store_eval(*c)
            

    def test_multi_proc_write(self):
        cases = [('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0.0),
                 ('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 2 21', 10.66),
                 ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34', -25)]
        store_path = None
        def write_process(fen, eval, process_id, grug):
            name = f'Process-{process_id}'
            result = grug.store_eval(fen, eval)
            print(f'Process {name} results: {result}')
        if __name__ == 'src.testing.test_grug_eval':
            print('\nrunning test multi proc grug\n')
            GrugManager.register('GrugEvalStore', GrugEvalStore)
            with GrugManager() as gm:
                grug_store = gm.GrugEvalStore()
                store_path = grug_store.get_path()
                processes = []
                for i in range(3):
                    p = mp.Process(target=write_process, args=(*cases[i], i, grug_store))
                    processes.append(p)
                    p.start()

                for p in processes:
                    p.join()

                print('\n--Finished writing files--')

            ls_grug_dir = os.listdir(store_path)
            print(f'Current grug directory:\n{'\n'.join(ls_grug_dir)}')
            self.assertEqual(len(ls_grug_dir), 3)
            self.assertTrue('"rnbqkbnr=pppppppp=8=8=8=8=PPPPPPPP=RNBQKBNR_w_0.00".txt')
        else:
            print(f'\nnot running test multi proc grug: {__name__}')          

            
    def test_mp_write_collision(self):
        cases = [('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0.0),
                 ('5rk1/pppb1p1p/3p2p1/3P2N1/2P2P1q/3B3P/PP1Q1bPK/5R2 b - - 2 21', 10.66),
                 ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34', -25),
                 ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34', -25)]
        store_path = None
        def write_process(fen, eval, process_id, grug):
            name = f'Process-{process_id}'
            result = grug.store_eval(fen, eval)
            print(f'Process {name} results: {result}')
        if __name__ == 'src.testing.test_grug_eval':
            print('\nrunning test multi proc grug\n')
            GrugManager.register('GrugEvalStore', GrugEvalStore)
            with GrugManager() as gm:
                grug_store = gm.GrugEvalStore()
                store_path = grug_store.get_path()
                processes = []
                for i in range(len(cases)):
                    p = mp.Process(target=write_process, args=(*cases[i], i, grug_store))
                    processes.append(p)
                    p.start()

                for p in processes:
                    p.join()

                print('\n--Finished writing files--')

            ls_grug_dir = os.listdir(store_path)
            print(f'Current grug directory:\n{'\n'.join(ls_grug_dir)}')
            self.assertEqual(len(ls_grug_dir), 3)
            self.assertTrue('"rnbqkbnr=pppppppp=8=8=8=8=PPPPPPPP=RNBQKBNR_w_0.00".txt')
            self.assertTrue('"6R1=8=2B5=4Q3=P1k2P1P=8=3K4=8_w_-25.00".txt')
        else:
            print(f'\nnot running test multi proc grug: {__name__}')         