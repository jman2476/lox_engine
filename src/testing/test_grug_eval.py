import unittest
from src.eval_store import GrugEvalStore
import os, shutil


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
        expected = ['k7/3Q4/K7/8/8/8/8/8_w_69.42.txt',
                    '6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8_w_-420.69.txt']

        for i in range(2):
            file_name = grug_eval.create_file_name(*cases[i])
            self.assertEqual(file_name, expected[i])


    def test_parse_file_name(self):
        cases = ['k7/3Q4/K7/8/8/8/8/8_w_69.42.txt',
                '6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8_w_-420.69.txt']
        expected = [('k7/3Q4/K7/8/8/8/8/8','w',69.42),
                    ('6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8','w',-420.69)]
        grug_eval = GrugEvalStore()

        for i in range(2):
            parsed_file = grug_eval.parse_file_name(cases[i])
            self.assertEqual(parsed_file, expected[i])
