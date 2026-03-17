from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square

def find_available_moves(board, piece):
    moves = set()

    match type(piece):
        case Pawn():
            moves.update(find_pawn_moves(board, piece))
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

def find_pawn_moves(board, pawn):
    rank_to_check = pawn.rank + 1 if pawn.side == 'white' else pawn.rank - 1

def find_king_moves(board, pawn):
    pass

def find_knight_moves(board, pawn):
    pass

def find_queen_moves(board, pawn):
    pass

def find_rook_moves(board, pawn):
    pass

def find_bishop_moves(board, pawn):
    pass
