import unittest
from src.functions.linears import (get_horizontal_squares,
                                   get_vertical_squares)

class TestLinears(unittest.TestCase):
    def test_get_horizontal_squares(self):
        edges_1 = ['a1', 'h1']
        edges_2 = ['b2', 'c2']
        edges_3 = ['c3', 'g3']
        edges_4 = ['b4', 'd4']

        squares_1 = get_horizontal_squares(*edges_1)
        self.assertEqual(
            squares_1, 
            ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        )

        squares_2 = get_horizontal_squares(*edges_2)
        self.assertEqual(
            squares_2, 
            ['b2', 'c2']
        )

        squares_3 = get_horizontal_squares(*edges_3)
        self.assertEqual(
            squares_3, 
            ['c3', 'd3', 'e3', 'f3', 'g3']
        )

        squares_4 = get_horizontal_squares(*edges_4)
        self.assertEqual(
            squares_4, 
            ['b4', 'c4', 'd4']
        )

        with self.assertRaises(ValueError):
            squares_5 = get_vertical_squares('d4', 'g8')
            print(squares_5)


    def test_get_vertical_squares(self):
        edges_1 = ['a1', 'a8']
        edges_2 = ['b2', 'b6']
        edges_3 = ['c3', 'c3']
        edges_4 = ['d4', 'd7']
        
        squares_1 = get_vertical_squares(*edges_1)
        self.assertEqual(
            squares_1, 
            ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
        )

        squares_2 = get_vertical_squares(*edges_2)
        self.assertEqual(
            squares_2, 
            ['b2', 'b3', 'b4', 'b5', 'b6']
        )

        squares_3 = get_vertical_squares(*edges_3)
        self.assertEqual(
            squares_3, 
            ['c3']
        )

        squares_4 = get_vertical_squares(*edges_4)
        self.assertEqual(
            squares_4, 
            [ 'd4', 'd5', 'd6', 'd7']
        )
        
        with self.assertRaises(ValueError):
            squares_5 = get_vertical_squares('d4', 'g8')
            print(squares_5)