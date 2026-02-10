import unittest
from src.functions.diagonals import get_diagonal_edges

class TestDiagonals(unittest.TestCase):
    def test_get_back_diagonal(self):
        left_edge, right_edge = get_diagonal_edges('back')('e', 2)

        self.assertEqual(
            left_edge, ['a',6]
        )
        self.assertEqual(
            right_edge, ['f',1]
        )
        
        left_edge, right_edge = get_diagonal_edges('back')('c', 5)

        self.assertEqual(
            left_edge, ['a',7]
        )
        self.assertEqual(
            right_edge, ['g',1]
        )
        
    def test_get_forward_diagonal(self):
        left_edge, right_edge = get_diagonal_edges('forward')('e', 2)

        self.assertEqual(
            left_edge, ['d',1]
        )
        self.assertEqual(
            right_edge, ['h',5]
        )
        
        left_edge, right_edge = get_diagonal_edges('forward')('c', 5)

        self.assertEqual(
            left_edge, ['a',3]
        )
        self.assertEqual(
            right_edge, ['f',8]
        )
        