

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
        print(self.board)
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
                    dark = not dark if key is not 'h' else dark
                rank += f' {piece} '
            board += rank + '\n'

        return board
