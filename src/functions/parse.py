def parse_square(self, square_string):
        (file, rank) = (square_string[0], square_string[1])
        if ord(rank) not in range(49, 57):
            raise ValueError('parse_square: rank not between 1 and 8')
        if ord(file) not in range(97, 105) and ord(file) not in range(65, 72):
            raise ValueError('parse_square: file not between a and h, or A and H')
        # print(f'Good square: {file}{ord(rank) - 48}')
        return file, ord(rank) - 48