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
            rank = 1
            while rank <= 8:
                if key == 'a' or key == 'h':
                    match rank:
                        case 1:
                            file[rank-1] = Rook('white', f'{key}{rank}')
                        case 2:
                            file[rank-1] = Pawn('white', f'{key}{rank}')
                        case 7:
                            file[rank-1] = Pawn('black', f'{key}{rank}')
                        case 8:
                            file[rank-1] = Rook('black', f'{key}{rank}')
                elif key == 'b' or key == 'g':
                    match rank:
                        case 1:
                            file[rank-1] = Knight('white', f'{key}{rank}')
                        case 2:
                            file[rank-1] = Pawn('white', f'{key}{rank}')
                        case 7:
                            file[rank-1] = Pawn('black', f'{key}{rank}')
                        case 8:
                            file[rank-1] = Knight('black', f'{key}{rank}')
                elif key == 'c' or key == 'f':
                    match rank:
                        case 1:
                            file[rank-1] = Bishop('white', f'{key}{rank}')
                        case 2:
                            file[rank-1] = Pawn('white', f'{key}{rank}')
                        case 7:
                            file[rank-1] = Pawn('black', f'{key}{rank}')
                        case 8:
                            file[rank-1] = Bishop('black', f'{key}{rank}')
                elif key == 'd':
                    match rank:
                        case 1:
                            file[rank-1] = Queen('white', f'{key}{rank}')
                        case 2:
                            file[rank-1] = Pawn('white', f'{key}{rank}')
                        case 7:
                            file[rank-1] = Pawn('black', f'{key}{rank}')
                        case 8:
                            file[rank-1] = Queen('black', f'{key}{rank}')
                elif key == 'e':
                    match rank:
                        case 1:
                            file[rank-1] = King('white', f'{key}{rank}')
                        case 2:
                            file[rank-1] = Pawn('white', f'{key}{rank}')
                        case 7:
                            file[rank-1] = Pawn('black', f'{key}{rank}')
                        case 8:
                            file[rank-1] = King('black', f'{key}{rank}')


                if (rank == 2): rank = 7
                else: rank += 1

                            