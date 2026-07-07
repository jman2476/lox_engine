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
            moves.update(pawn_squares_controlled(board, piece))
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
