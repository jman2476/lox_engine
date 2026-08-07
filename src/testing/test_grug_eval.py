import unittest
from src.eval_store import GrugEvalStore
import os, shutil


class TestGrugEval(unittest.TestCase):
    def test_grug_mkdir(self):
        grug_eval_a = GrugEvalStore()
        self.assertEqual(os.path.exists('./grug_eval'), True)
        grug_a_ls = os.listdir('./grug_eval')
        print(f'Grug a contents: {grug_a_ls}')
        self.assertEqual(len(grug_a_ls), 0)

        grug_eval_b = GrugEvalStore('./grug_eval_2')
        self.assertEqual(os.path.exists('./grug_eval_2'), True)
        grug_b_ls = os.listdir('./grug_eval_2')
        print(f'Grug a contents: {grug_b_ls}')
        self.assertEqual(len(grug_b_ls), 0)

        dummy_file_path = os.path.join(grug_eval_a.path, 'test.txt')
        with open(dummy_file_path, 'w', encoding='UTF-8') as file:
            file.write('Potato test')
        grug_a_ls = os.listdir('./grug_eval')
        print(f'Grug a contents: {grug_a_ls}')
        self.assertEqual(len(grug_a_ls), 1)

        grug_eval_a_2 = GrugEvalStore()
        grug_a_ls = os.listdir('./grug_eval')
        print(f'Grug a contents: {grug_a_ls}')
        self.assertEqual(len(grug_a_ls), 0)

        shutil.rmtree(grug_eval_a_2.path)
        shutil.rmtree(grug_eval_b.path)