import unittest
from src.functions.parse import parse_square

class TestParse(unittest.TestCase):
    def test_parse_square(self):
        self.assertEqual(parse_square('a1'), ('a',1))
        self.assertEqual(parse_square('A1'), ('a',1))
        self.assertEqual(parse_square('b3'), ('b',3))
        self.assertEqual(parse_square('B3'), ('b',3))
        self.assertEqual(parse_square('g8'), ('g',8))
        self.assertEqual(parse_square('G8'), ('g',8))

        with self.assertRaises(
                ValueError, 
                msg='parse_square: file not between a and h, or A and H'
                ):
            parse_square('r5')
            parse_square('R5')

        with self.assertRaises(
                ValueError,
                msg='parse_square: rank not between 1 and 8'
                ):
            parse_square('n9')
            parse_square('N9')
            parse_square('h0')
            parse_square('H0')

        with self.assertRaises(
                ValueError,
                msg='parse_square: square_string is too long, should be 2 characters'
                ):
            parse_square('a10')




if __name__ == '__main__':
    unittest.main()

