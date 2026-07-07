# Similar to find_moves.py, but finding how many squares are controlled,
#  not what moves a piece can do. Main difference will be for king and pawn
from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )

def find_squares_controlled(board, piece):
    moves = set()

    match piece:
        case Pawn():
            pass
        case King():
            pass
        case Queen():
            pass
        case Bishop():
            pass
        case Rook():
            pass
        case Knight():
            pass
    return moves

def pawn_squares_controlled(board, piece):
    ...


def king_squares_controlled(board, piece):
    ...


def queen_squares_controlled(board, piece):
    ...


def bishop_squares_controlled(board, piece):
    ...


def knight_squares_controlled(board, piece):
    ...

    
def rook_squares_controlled(board, piece):
    ...
