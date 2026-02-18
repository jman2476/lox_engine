import unittest
from src.functions.diagonals import (get_diagonal_edges,
                                     get_diagonal_squares)

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
        
        left_edge, right_edge = get_diagonal_edges('back')('h', 8)

        self.assertEqual(
            left_edge, ['a', 1]
        )

        self.assertEqual(
            right_edge, ['h', 8]
        )

        left_edge, right_edge = get_diagonal_edges('back')('a', 1)

        self.assertEqual(
            left_edge, ['a', 1]
        )

        self.assertEqual(
            right_edge, ['h', 8]
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
        
        left_edge, right_edge = get_diagonal_edges('forward')('a', 8)

        self.assertEqual(
            left_edge, ['a', 8]
        )

        self.assertEqual(
            right_edge, ['h', 1]
        )

        left_edge, right_edge = get_diagonal_edges('forward')('h', 1)

        self.assertEqual(
            left_edge, ['a', 8]
        )

        self.assertEqual(
            right_edge, ['h', 1]
        )
        

    def test_get_diagonal_squares(self):
        e7_arr = get_diagonal_squares(
            *get_diagonal_edges('back')('e',7)
        )
        h3_arr = get_diagonal_squares(
            *get_diagonal_edges('forward')('h',3)
        )
        d4_b_arr = get_diagonal_squares(
            *get_diagonal_edges('back')('d',4)
        )
        d4_f_arr = get_diagonal_squares(
            *get_diagonal_edges('forward')('d',4)
        )

        self.assertEqual(
            e7_arr,
            [('d',8),('e',7),('f',6),('g',5),('h',4)]
        )
        self.assertEqual(
            h3_arr,
            [('f',1),('g',2),('h',3)]
        )
        self.assertEqual(
            d4_b_arr,
            [('a',7),('b',6),('c',5),('d',4),('e',3),('f',2),('g',1)]
        )
        self.assertEqual(
            d4_f_arr,
            [('a',1),('b',2),('c',3),('d',4),('e',5),('f',6),('g',7),('h',8)]
        )