from .piece import Piece, Pawn, King, Queen, Bishop, Knight, Rook

class Board():
    def __init__(self):
        self.board = {
                "a":[None for i in range(0,8)],
                "b":[None for i in range(0,8)],
                "c":[None for i in range(0,8)],
                "d":[None for i in range(0,8)],
                "e":[None for i in range(0,8)],
                "f":[None for i in range(0,8)],
                "g":[None for i in range(0,8)],
                "h":[None for i in range(0,8)],
                }
        self.ranks = [i for i in range(0,8)]
        self.files = list("abcdefgh")
        self.frame = (self.ranks, self.files)
        

    def __repr__(self):
        dark = True
        files = '   '
        board = ''
        # Print files:
        for f in self.files:
            files += f' {f} '
        board += files + '\n'

        # Print ranks:
        for r in self.ranks:
            rank = f'{r+1} —'
            for key, file in self.board.items():
                piece = file[r]
                if piece is None: 
                    piece = '\u25A0' if dark else '\u25A1'
                else:
                    piece = piece.icon
                dark = not dark if key != 'h' else dark
                rank += f' {piece} '
            board += rank + '\n'

        return board

    def setup_new(self):
        for key, file in self.board.items():
            file[0] = self.set_back_rank(key)('white', f'{key}1')
            file[1] = Pawn('white', f'{key}2')
            file[6] = Pawn('black', f'{key}7')
            file[7] = self.set_back_rank(key)('black', f'{key}8')
            

    def set_back_rank(self, file):
        if file == 'a' or file == 'h':
            return Rook
        if file == 'b' or file == 'g':
            return Knight
        if file == 'c' or file == 'f':
            return Bishop
        if file == 'd':
            return Queen
        if file == 'e':
            return King
        raise ValueError('set_back_rank: File value given is out of range')