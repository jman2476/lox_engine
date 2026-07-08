# Similar to find_moves.py, but finding how many squares are controlled,
#  not what moves a piece can do. Main difference will be for king and pawn
from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )

class ControlledSquares():
    def __init__(self):
        self.squares = {}

    def add(self, squares:list[str]):
        for sq in squares:
            if sq in self.squares:
                self.squares[sq] += 1
            else:
                self.squares[sq] = 1

def find_squares_controlled(board, piece):
    moves = ControlledSquares()

    match piece:
        case Pawn():
            moves.add(pawn_squares_controlled(board, piece))
        case King():
            moves.update(king_squares_controlled(board, piece))
        case Queen():
            moves.update(queen_squares_controlled(board, piece))
        case Bishop():
            moves.update(bishop_squares_controlled(board, piece))
        case Rook():
            moves.update(rook_squares_controlled(board, piece))
        case Knight():
            moves.update(knight_squares_controlled(board, piece))
    return moves

def pawn_squares_controlled(board, pawn) -> list[str]:
    file, rank = pawn.file, pawn.rank
    direction = 1 if pawn.side == 'white' else -1
    f_idx = board.files.index(file)
    files_to_check = [board.files[j] for j in 
                      [i + f_idx for i in range(-1,2) 
                       if i != 0] if j in range(0,8)]
    return [f'{f}{rank+direction}' for f in files_to_check]

def king_squares_controlled(board, king) -> list[str]:
    file, rank = king.file, king.rank
    f_idx = board.files.index(file)
    return [f'{board.files[f]}{r}' for f in [f_idx+i for i in range(-1,2)] 
               for r in [r+i for i in range(-1,2)]
               if f != f_idx or r != rank]


def queen_squares_controlled(board, queen) -> list[str]:
    ...


def bishop_squares_controlled(board, piece) -> list[str]:
    ...


def knight_squares_controlled(board, knight) -> list[str]:
    return board.bound_squares('knight', True)(
        knight.file,
        knight.rank,
        knight.side
    )


def rook_squares_controlled(board, piece) -> list[str]:
    ...
